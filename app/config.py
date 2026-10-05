from dataclasses import dataclass
import os


def _bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_version: str
    host: str
    port: int
    database_url: str

    llm_provider: str
    llm_base_url: str
    llm_api_key: str
    llm_model: str

    messaging_enabled: bool
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_endpoint_url: str
    sqs_queue_url: str
    sns_topic_arn: str

    fault_mode: str
    fault_delay_ms: int


def load_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "JobScout AI"),
        app_version=os.getenv("APP_VERSION", "0.1.0"),
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./data/jobscout.db"),
        llm_provider=os.getenv("LLM_PROVIDER", "mock"),
        llm_base_url=os.getenv("LLM_BASE_URL", "").rstrip("/"),
        llm_api_key=os.getenv("LLM_API_KEY", ""),
        llm_model=os.getenv("LLM_MODEL", ""),
        messaging_enabled=_bool("MESSAGING_ENABLED", False),
        aws_region=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        aws_endpoint_url=os.getenv("AWS_ENDPOINT_URL", "").rstrip("/"),
        sqs_queue_url=os.getenv("SQS_QUEUE_URL", ""),
        sns_topic_arn=os.getenv("SNS_TOPIC_ARN", ""),
        fault_mode=os.getenv("FAULT_MODE", "none").lower().strip(),
        fault_delay_ms=int(os.getenv("FAULT_DELAY_MS", "0")),
    )
