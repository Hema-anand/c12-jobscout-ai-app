from dataclasses import dataclass
import logging
import re
import time
from typing import Callable, Iterable

from app.config import Settings
from app.db.models import Job
from app.llm.provider import LLMProvider
from app.observability.metrics import LLM_CALLS

LOGGER = logging.getLogger(__name__)

STOPWORDS = {
    "a", "an", "and", "are", "at", "be", "for", "from", "i", "in",
    "me", "my", "of", "on", "or", "please", "the", "to", "with",
    "find", "looking", "want", "need", "jobs", "job", "role", "roles",
}


@dataclass(frozen=True)
class AgentStepEvent:
    step_name: str
    started_at: float
    duration_ms: float
    metadata: dict


StepObserver = Callable[[AgentStepEvent], None]


class JobSearchAgent:
    """Small, deliberately transparent multi-step workflow.

    The workflow is kept explicit so later course sprints can instrument
    individual steps with Langfuse and OpenTelemetry without rewriting
    application behavior.
    """

    def __init__(
        self,
        session,
        llm: LLMProvider,
        settings: Settings,
        observer: StepObserver | None = None,
    ):
        self.session = session
        self.llm = llm
        self.settings = settings
        self.observer = observer

    def _run_step(self, name: str, fn, **metadata):
        if self.settings.fault_mode == "slow" and name in {
            "retrieve_jobs",
            "rank_jobs",
            "generate_response",
        }:
            if self.settings.fault_delay_ms > 0:
                time.sleep(self.settings.fault_delay_ms / 1000)

        started = time.perf_counter()
        result = fn()
        duration_ms = (time.perf_counter() - started) * 1000

        event = AgentStepEvent(
            step_name=name,
            started_at=started,
            duration_ms=duration_ms,
            metadata=metadata,
        )
        if self.observer:
            self.observer(event)

        LOGGER.info(
            "agent_step_complete step=%s duration_ms=%.2f",
            name,
            duration_ms,
        )
        return result

    def parse_query(self, message: str) -> list[str]:
        tokens = re.findall(r"[a-zA-Z0-9+#.-]+", message.lower())
        return [token for token in tokens if token not in STOPWORDS and len(token) > 1]

    def retrieve_jobs(self) -> list[Job]:
        return list(self.session.query(Job).all())

    def rank_jobs(self, jobs: Iterable[Job], terms: list[str]) -> list[tuple[Job, float]]:
        ranked = []

        for job in jobs:
            title = job.title.lower()
            location = job.location.lower()
            skill_text = job.skills.lower().replace(",", " ")
            description = job.description.lower()

            score = 0.0
            for term in terms:
                if term in title:
                    score += 4
                if term in location:
                    score += 3
                if term in skill_text:
                    score += 3
                if term in description:
                    score += 1

            if score > 0:
                ranked.append((job, score))

        ranked.sort(key=lambda item: (-item[1], item[0].id))
        return ranked

    def generate_response(self, message: str, ranked: list[tuple[Job, float]]) -> str:
        jobs = [job for job, _ in ranked[:5]]
        if self.settings.fault_mode == "llm_error":
            raise RuntimeError("Seeded LLM failure.")
        LLM_CALLS.labels(self.llm.name).inc()
        return self.llm.generate(message, jobs)

    def search(self, message: str) -> tuple[str, list[Job]]:
        terms = self._run_step(
            "parse_request",
            lambda: self.parse_query(message),
        )
        jobs = self._run_step(
            "retrieve_jobs",
            self.retrieve_jobs,
            term_count=len(terms),
        )
        ranked = self._run_step(
            "rank_jobs",
            lambda: self.rank_jobs(jobs, terms),
            job_count=len(jobs),
        )
        response = self._run_step(
            "generate_response",
            lambda: self.generate_response(message, ranked),
            match_count=min(len(ranked), 5),
        )
        return response, [job for job, _ in ranked[:5]]
