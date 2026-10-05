import logging
import time
import uuid

from fastapi import APIRouter, HTTPException, Request
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from fastapi.responses import PlainTextResponse
from sqlalchemy import text

from app.agent.service import JobSearchAgent
from app.api.schemas import ChatRequest, ChatResponse, HealthResponse
from app.db.models import ChatEvent, ChatSession
from app.llm.provider import build_llm
from app.messaging.publisher import MessagingPublisher
from app.observability.metrics import (
    CHAT_DURATION,
    CHAT_ERRORS,
    CHAT_MATCHES,
    CHAT_REQUESTS,
)

LOGGER = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health(request: Request):
    session_factory = request.app.state.session_factory
    with session_factory() as session:
        session.execute(text("SELECT 1"))

    settings = request.app.state.settings
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
    )


@router.get("/metrics")
def metrics():
    return PlainTextResponse(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, request: Request):
    started = time.perf_counter()
    request_id = uuid.uuid4().hex
    settings = request.app.state.settings
    session_factory = request.app.state.session_factory

    CHAT_REQUESTS.inc()

    try:
        with session_factory() as session:
            if settings.fault_mode == "db_error":
                raise RuntimeError("Seeded database failure.")

            agent = JobSearchAgent(
                session=session,
                llm=request.app.state.llm,
                settings=settings,
            )
            answer, jobs = agent.search(payload.message)

            chat_session = ChatSession(
                request_id=request_id,
                query=payload.message,
                response=answer,
            )
            session.add(chat_session)
            session.commit()

            messaging_result = {"sqs": False, "sns": False}
            if settings.messaging_enabled:
                if settings.fault_mode == "queue_error":
                    raise RuntimeError("Seeded queue publishing failure.")

                publisher = MessagingPublisher(settings)
                messaging_result = publisher.publish_search_completed(
                    request_id=request_id,
                    query=payload.message,
                    match_ids=[job.id for job in jobs],
                )

                for destination, published in messaging_result.items():
                    session.add(
                        ChatEvent(
                            request_id=request_id,
                            event_type="job_search.completed",
                            destination=destination,
                            published=int(published),
                        )
                    )
                session.commit()

            CHAT_MATCHES.observe(len(jobs))

            return ChatResponse(
                request_id=request_id,
                answer=answer,
                matched_jobs=[
                    {
                        "id": job.id,
                        "title": job.title,
                        "company": job.company,
                        "location": job.location,
                    }
                    for job in jobs
                ],
                messaging=messaging_result,
            )

    except Exception as exc:
        CHAT_ERRORS.inc()
        LOGGER.exception("chat_failed request_id=%s", request_id)
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    finally:
        CHAT_DURATION.observe(time.perf_counter() - started)
