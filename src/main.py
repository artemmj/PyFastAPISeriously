import loguru
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.auth.router.auth import router as auth_router
from src.auth.router.users import router as users_router
from src.purchase.products.router.products import router as products_router
from src.purchase.products.router.product_category import router as product_category_router
from src.purchase.cart.router import router as carts_router
from src.purchase.order.router import router as orders_router

logger = loguru.logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    """Application lifecycle management."""
    # logger.info("Инициализация приложения...")
    yield
    # logger.info("Завершение работы приложения...")


def register_routers(app: FastAPI) -> None:
    app.include_router(auth_router, prefix='/api/auth', tags=["Авторизация и аутентификация"])
    app.include_router(users_router, prefix='/api/users', tags=["Пользователи"])
    app.include_router(products_router, prefix='/api/products', tags=["Товары"])
    app.include_router(product_category_router, prefix='/api/products/categories', tags=["Категории товаров"])
    app.include_router(carts_router, prefix='/api/carts', tags=["Корзины товаров"])
    app.include_router(orders_router, prefix='/api/orders', tags=["Заказы"])


def add_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins='*',  # допущенные к API домены
        allow_credentials=True,  # позволяет передавать куки
        allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
        allow_headers=[  # HTTP-заголовки
            'access_token',
            "Content-Type",
            "Set-Cookie",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin",
            "Authorization",
        ],
    )


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Проект на FastAPI",
        version="0.0.1",
        description="",
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )
    app.mount("/static", StaticFiles(directory="static"), name="static")
    register_routers(app)
    add_middlewares(app)
    return app


# Создание экземпляра приложения
app = create_app()
