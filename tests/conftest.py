import pytest_asyncio
import httpx

from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.auth.models import Role, RolesEnum
from src.dao.base_model import Base
from src.dao.database import get_session_with_commit, get_session_without_commit
from src.main import app 
from src.settings import settings

DATABASE_URL_TEST = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/test_db"
fake = Faker()


@pytest_asyncio.fixture(scope="session")
def faker_instance():
    return Faker(locale='ru_RU')


@pytest_asyncio.fixture(scope="function")
async def clean_db():
    # Создаем асинхронный движок *внутри* фикстуры
    engine = create_async_engine(DATABASE_URL_TEST)
    # AsyncSessionLocal для тестов
    TestAsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:  # Создаем таблицы перед тестами
        await conn.run_sync(Base.metadata.create_all)

    async with TestAsyncSessionLocal() as session:   # Заполняем таблицу roles начальными данными
        async with session.begin():
            roles_to_insert = [{"name": role.name} for role in RolesEnum]
            from sqlalchemy import insert
            stmt = insert(Role).values(roles_to_insert)
            await session.execute(stmt)
        await session.commit() # Подтверждаем вставку ролей

    yield engine

    async with engine.begin() as conn:  # Очищаем таблицы после теста
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()  # Закрываем движок


# --- Асинхронная фикстура для тестовой асинхронной сессии БД ---
@pytest_asyncio.fixture(scope="function")
async def async_db_session(clean_db): # Зависимость от clean_db
    engine = clean_db # Получаем engine из фикстуры clean_db
    TestAsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with TestAsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# --- Асинхронная фикстура для асинхронного клиента ---
@pytest_asyncio.fixture(scope="function")
async def async_client(async_db_session):

    def override_get_session_without_commit():
        yield async_db_session

    def override_get_session_with_commit():
        yield async_db_session

    app.dependency_overrides[get_session_with_commit] = override_get_session_with_commit
    app.dependency_overrides[get_session_without_commit] = override_get_session_without_commit

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# --- Фикстура для генерации стандартных данных пользователя ---
@pytest_asyncio.fixture
async def standard_user_data(faker_instance):
    """Генерирует стандартный набор данных для пользователя."""
    return {
        "first_name": faker_instance.first_name(),
        "last_name": faker_instance.last_name(),
        "email": faker_instance.email(),
        "phone_number": '+' + faker_instance.phone_number(),
        "password": "12345",
        "confirm_password": "12345"
    }


# --- Фикстура для генерации данных с невалидным email ---
@pytest_asyncio.fixture
async def invalid_email_user_data(faker_instance):
    """Генерирует данные пользователя с невалидным email."""
    return {
        "first_name": faker_instance.first_name(),
        "last_name": faker_instance.last_name(),
        "email": "not-an-email",
        "phone_number": '+' + faker_instance.phone_number(),
        "password": "12345",
        "confirm_password": "12345"
    }


# --- Фикстура для генерации данных с длинным именем ---
@pytest_asyncio.fixture
async def long_name_user_data(faker_instance):
    """Генерирует данные пользователя с длинным именем."""
    return {
        "first_name": faker_instance.text(max_nb_chars=200),
        "last_name": faker_instance.last_name(),
        "email": faker_instance.email(),
        "phone_number": '+' + faker_instance.phone_number(),
        "password": "12345",
        "confirm_password": "12345"
    }


@pytest_asyncio.fixture
async def registered_user(async_client, standard_user_data):
    standard_user_data.pop('confirm_password')
    response = await async_client.post("/auth/register", json=standard_user_data)
    assert response.status_code == 201
    return response.json()
