from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.infra.bootstrap import Container
from src.infra.config import get_settings
from src.infra.db import create_engine, create_session_factory
from src.infra.logging.setup import setup_logging


class HealthResponse(BaseModel):
    success: bool = Field(
        default=True,
        description="Флаг успешности запроса",
        examples=[True],
    )
    status: str = Field(
        default="ok",
        description="Текущее состояние приложения",
        examples=["ok"],
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    setup_logging(settings.app)

    engine = create_engine(settings.db)
    session_factory = create_session_factory(engine)
    container = Container(
        settings=settings,
        session_factory=session_factory,
    )

    app.state.container = container

    try:
        yield
    finally:
        await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Your API",
        version="1.0.0",
        lifespan=lifespan,
    )

    @app.get(
        "/health",
        response_model=HealthResponse,
        summary="Проверка доступности приложения",
        description="Возвращает простой health response для проверки, что API запущено и принимает запросы.",
    )
    async def health() -> HealthResponse:
        return HealthResponse()

    return app


app = create_app()
