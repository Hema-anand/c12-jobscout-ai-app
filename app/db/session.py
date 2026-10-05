from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import Settings, load_settings
from app.db.base import Base


def build_engine(settings: Settings):
    connect_args = {}
    if settings.database_url.startswith("sqlite"):
        Path("data").mkdir(parents=True, exist_ok=True)
        connect_args["check_same_thread"] = False
    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
        connect_args=connect_args,
    )


settings = load_settings()
engine = build_engine(settings)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db() -> None:
    import app.db.models  # noqa: F401
    Base.metadata.create_all(bind=engine)
