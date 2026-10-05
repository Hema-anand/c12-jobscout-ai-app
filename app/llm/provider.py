from dataclasses import dataclass

import httpx

from app.config import Settings
from app.db.models import Job


class LLMProvider:
    name = "base"

    def generate(self, user_message: str, jobs: list[Job]) -> str:
        raise NotImplementedError


class MockLLM(LLMProvider):
    name = "mock"

    def generate(self, user_message: str, jobs: list[Job]) -> str:
        if not jobs:
            return (
                "I could not find a strong match in the current sample job catalog. "
                "Try adding a skill, role, or location to your request."
            )

        lines = [
            f"I found {len(jobs)} relevant role(s) for: {user_message}",
            "",
            "Top matches:",
        ]
        for index, job in enumerate(jobs[:5], start=1):
            lines.append(
                f"{index}. {job.title} at {job.company} - {job.location}"
            )
        lines.extend(
            [
                "",
                "The results are based on the skills, role words, and location "
                "signals present in your request."
            ]
        )
        return "\n".join(lines)


class OpenAICompatibleLLM(LLMProvider):
    name = "openai_compatible"

    def __init__(self, settings: Settings):
        if not settings.llm_base_url or not settings.llm_api_key or not settings.llm_model:
            raise ValueError(
                "LLM_BASE_URL, LLM_API_KEY and LLM_MODEL are required "
                "for the openai_compatible provider."
            )
        self.base_url = settings.llm_base_url
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model

    def generate(self, user_message: str, jobs: list[Job]) -> str:
        job_context = "\n".join(
            f"- {job.title} | {job.company} | {job.location} | {job.skills}"
            for job in jobs[:5]
        )

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a concise job-search assistant. "
                        "Use only the supplied job matches. "
                        "Do not invent openings."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"User request: {user_message}\n\n"
                        f"Matching jobs:\n{job_context}\n\n"
                        "Summarize the strongest matches."
                    ),
                },
            ],
            "temperature": 0.2,
        }

        with httpx.Client(timeout=30) as client:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        return data["choices"][0]["message"]["content"]


def build_llm(settings: Settings) -> LLMProvider:
    provider = settings.llm_provider.lower()
    if provider == "mock":
        return MockLLM()
    if provider == "openai_compatible":
        return OpenAICompatibleLLM(settings)
    raise ValueError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")
