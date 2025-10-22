from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger

from src.auth.router import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    """Управление жизненным циклом приложения."""
    # logger.info("Инициализация приложения...")
    yield
    # logger.info("Завершение работы приложения...")


def register_routers(app: FastAPI) -> None:
    """Регистрация роутеров приложения."""
    app.include_router(auth_router, prefix='/auth', tags=["Auth / Users"])


def create_app() -> FastAPI:
    """Создание и конфигурация FastAPI приложения."""
    app = FastAPI(
        title="Проект FastAPI",
        version="0.0.1",
        description="Такой вот проект",
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )
    register_routers(app)
    return app

# Создание экземпляра приложения
app = create_app()
