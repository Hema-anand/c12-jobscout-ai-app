from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


class MatchedJob(BaseModel):
    id: int
    title: str
    company: str
    location: str


class ChatResponse(BaseModel):
    request_id: str
    answer: str
    matched_jobs: list[MatchedJob]
    messaging: dict[str, bool]


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
