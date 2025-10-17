from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    """Управление жизненным циклом приложения."""
    logger.info("Инициализация приложения...")
    yield
    logger.info("Завершение работы приложения...")


def create_app() -> FastAPI:
    """Создание и конфигурация FastAPI приложения."""
    app = FastAPI(title="Проект FastAPI", version="0.0.1", lifespan=lifespan, default_response_class=ORJSONResponse)
    return app

# Создание экземпляра приложения
app = create_app()
