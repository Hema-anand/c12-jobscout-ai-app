from contextlib import asynccontextmanager
import logging
import time
import uuid

from fastapi import FastAPI, Request

from app.api.routes import router
from app.config import load_settings
from app.db.session import SessionLocal, init_db
from app.jobs.catalog import seed_jobs
from app.llm.provider import build_llm
from app.observability.context import request_id_var
from app.observability.logging import configure_logging
from app.observability.metrics import HTTP_DURATION, HTTP_REQUESTS

configure_logging()
LOGGER = logging.getLogger(__name__)
settings = load_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    with SessionLocal() as session:
        seed_jobs(session)
    LOGGER.info("application_started version=%s", settings.app_version)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Course reference application for C12.",
    lifespan=lifespan,
)

app.state.settings = settings
app.state.session_factory = SessionLocal
app.state.llm = build_llm(settings)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex)
    token = request_id_var.set(request_id)

    started = time.perf_counter()
    status = 500
    route = request.url.path

    try:
        response = await call_next(request)
        status = response.status_code
        response.headers["X-Request-ID"] = request_id
        return response
    finally:
        duration = time.perf_counter() - started
        HTTP_DURATION.labels(request.method, route).observe(duration)
        HTTP_REQUESTS.labels(request.method, route, str(status)).inc()
        request_id_var.reset(token)


app.include_router(router)
