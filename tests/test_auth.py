import pytest
import httpx


# --- ИНТЕГРАЦИОННЫЕ ТЕСТЫ ---

class TestAuthIntegration:

    @pytest.mark.asyncio
    async def test_register_user_success(self, async_client, standard_user_data):
        """Тестирует успешную регистрацию пользователя."""
        response = await async_client.post("/api/auth/register", json=standard_user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == standard_user_data["email"]
        assert data["phone_number"] == standard_user_data["phone_number"]
        assert "id" in data
        assert "password" not in data
        assert "hashed_password" not in data

    @pytest.mark.asyncio
    async def test_register_user_duplicate_email(self, async_client, standard_user_data):
        """Тестирует ошибку при регистрации с существующим email."""
        response1 = await async_client.post("/api/auth/register", json=standard_user_data)
        assert response1.status_code == 201
        response2 = await async_client.post("/api/auth/register", json=standard_user_data)
        assert response2.status_code == 409

    @pytest.mark.asyncio
    async def test_login_success(self, async_client: httpx.AsyncClient, standard_user_data):
        """Тестирует успешную авторизацию и получение токена."""
        await async_client.post("/api/auth/register", json=standard_user_data)
        login_data = {
            "email": standard_user_data["email"],
            "password": standard_user_data["password"]
        }
        response = await async_client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert len(data["access_token"]) > 10

    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, async_client, standard_user_data):
        """Тестирует ошибку при авторизации с неверными данными."""
        login_data = {
            "email": standard_user_data["email"],
            "password": "wrongpassword" # Неверный пароль
        }
        response = await async_client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_user_not_found(self, async_client):
        """Тестирует ошибку при авторизации с несуществующим email."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "any_password"
        }
        response = await async_client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401


# --- ЮНИТ ТЕСТЫ ---

class TestAuthDAOUnit:

    @pytest.mark.asyncio
    async def test_create_user(self, async_db_session, standard_user_data):
        """Тестирует DAO функцию создания пользователя."""
        from src.auth.dao import UsersDAO
        from src.auth.schemas import UserModelRegisterSchema
        from src.auth.security import verify_password

        users_dao = UsersDAO(async_db_session)
        user_create_schema = UserModelRegisterSchema(**standard_user_data)
        user_dict = user_create_schema.model_dump()
        user_dict.pop('confirm_password')
        created_user = await users_dao.add(**user_dict)

        assert created_user.email == standard_user_data["email"]
        assert created_user.first_name == standard_user_data["first_name"]
        assert created_user.last_name == standard_user_data["last_name"]
        # Проверим, что пароль был захеширован, а не сохранен в открытом виде
        assert created_user.password != standard_user_data["password"]
        # Проверим, что хеш действительно валиден
        assert verify_password(standard_user_data["password"], created_user.password)

    @pytest.mark.asyncio
    async def test_get_all_users(self, async_db_session, standard_user_data):
        """Тестирует DAO функцию получения всех пользователей."""
        from src.auth.dao import UsersDAO
        from src.auth.filters import UserFilter
        from src.auth.schemas import UserModelRegisterSchema

        users_dao = UsersDAO(async_db_session)
        user_create_schema = UserModelRegisterSchema(**standard_user_data)
        user_dict = user_create_schema.model_dump()
        user_dict.pop('confirm_password')
        created_user = await users_dao.add(**user_dict)

        users_dao = UsersDAO(async_db_session)
        user_create_schema = UserModelRegisterSchema(**standard_user_data)
        user_dict = user_create_schema.model_dump()
        user_dict.pop('confirm_password')
        user_dict['email'] = 'test2@mail.ru'
        user_dict['phone_number'] = '+79999999902'
        created_user = await users_dao.add(**user_dict)

        retrieved_users = await users_dao.find_all(UserFilter())

        assert len(retrieved_users) == 2
        # assert retrieved_users[1].id == created_user.id
        # assert retrieved_users[1].email == created_user.email
