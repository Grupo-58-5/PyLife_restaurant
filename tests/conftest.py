import asyncio
from typing import AsyncGenerator
import pytest
from fastapi.testclient import TestClient
from sqlmodel import StaticPool, create_engine, SQLModel, Session, inspect, select
from src.auth.infraestructure.model.user_model import UserModel
from src.shared.db.database import get_session
from src.shared.infraestructure.adapters.bcrypt_hash_adapter import BcryptHashAdapter
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine


from src.main import app
from src.auth.domain.enum.role import Roles

# DATABASE_URL = "sqlite:///:memory:"
# engine = create_engine(
#     DATABASE_URL,
#     echo=True,
#     connect_args={"check_same_thread": False},
#     poolclass=StaticPool
# )

# # Override de la dependencia
# def get_session_override():
#     with Session(engine) as session:
#         print("Session de test: ",session)
#         yield session

# app.dependency_overrides[get_session] = get_session_override

# # Ejecutado antes de cada test
# @pytest.fixture(name="prepare_db")
# def prepare_db():
#     SQLModel.metadata.create_all(engine)

#     inspector = inspect(engine)
#     tables = inspector.get_table_names()
#     print("Tablas creadas:", tables)
#     yield
#     SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def get_token_admin(client):
    # Ejecutar función asincrónica para insertar el usuario
    async def insert_user():
        async for session in get_session():
            bash = BcryptHashAdapter()
            password = await bash.get_password_hashed('password')
            user = UserModel(name='Luigi',email='luigi@test.com', password=password, role=Roles.ADMIN)
            session.add(user)
            await session.commit()
            await session.refresh(user)

    asyncio.run(insert_user())

    # Login usando TestClient (sincrónico)
    form_data = {
        'username': 'luigi@test.com',
        'password': 'password'
    }
    response = client.post("/auth/log_in", data=form_data)
    token = response.json().get("access_token")
    return token

@pytest.fixture(scope="function")
def get_token_client(client):

    user = {"name": "test","email":"test@gmail.com","password": "password"}
    client.post("/auth/sign_up",json=user)

    form_data = {
        'username': 'test@gmail.com',
        'password': 'password'
    }
    response = client.post("/auth/log_in", data=form_data)
    token = response.json().get("access_token")
    return token