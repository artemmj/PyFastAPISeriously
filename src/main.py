import loguru
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.auth.router.auth import router as auth_router
from src.auth.router.users import router as users_router
from src.products.router import router as products_router

logger = loguru.logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    """Application lifecycle management."""
    # logger.info("Инициализация приложения...")
    yield
    # logger.info("Завершение работы приложения...")


def register_routers(app: FastAPI) -> None:
    app.include_router(auth_router, prefix='/auth', tags=["Авторизация и аутентификация"])
    app.include_router(users_router, prefix='/users', tags=["Пользователи"])
    app.include_router(products_router, prefix='/products', tags=["Товары"])


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Проект на FastAPI",
        version="0.0.1",
        description="",
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )
    register_routers(app)
    return app


# Создание экземпляра приложения
app = create_app()
