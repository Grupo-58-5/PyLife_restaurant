import asyncio
from datetime import datetime
from typing import AsyncGenerator
from uuid import UUID
import pytest
from fastapi.testclient import TestClient
from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel
from src.restaurants.infraestructure.model.table_model import TableModel
from src.shared.db.init_db import create_tables

from src.auth.infraestructure.model.user_model import UserModel
from src.shared.db.database import get_session
from src.shared.infraestructure.adapters.bcrypt_hash_adapter import BcryptHashAdapter

from src.main import app
from src.auth.domain.enum.role import Roles


@pytest.fixture(scope="session", autouse=False)
def create_async_tables():
    asyncio.run(create_tables())
    yield
    # Si quieres limpiar después de los tests:
    # async def drop_tables():
    #     async with engine.begin() as conn:
    #         await conn.run_sync(SQLModel.metadata.drop_all)
    # asyncio.run(drop_tables())


@pytest.fixture(scope="session")
def insert_users(create_async_tables):
    async def insert_admin():
        async for session in get_session():
            bash = BcryptHashAdapter()
            password = await bash.get_password_hashed('password')
            user = UserModel(name='Luigi', email='luigi@test.com', password=password, role=Roles.ADMIN)
            session.add(user)
            await session.commit()
            await session.refresh(user)
    asyncio.run(insert_admin())

    async def insert_client():
        async for session in get_session():
            bash = BcryptHashAdapter()
            password = await bash.get_password_hashed('password')
            user = UserModel(name='Test', email='test@gmail.com', password=password, role=Roles.CLIENT)
            session.add(user)
            await session.commit()
            await session.refresh(user)
    asyncio.run(insert_client())

@pytest.fixture(scope="session")
def insert_restaurant(create_async_tables) -> (tuple[UUID | None, UUID] | None):
    print("Ejecutando Fixture")
    async def insert():
        async for session in get_session():
            restaurant = RestaurantModel(
                name='Luigi',
                location='Vista Alegre',
                opening_time=datetime.strptime('08:00:00', "%H:%M:%S").time(),
                closing_time=datetime.strptime('22:00:00', "%H:%M:%S").time()
            )
            session.add(restaurant)
            await session.commit()
            await session.refresh(restaurant)
            table = TableModel(
                table_number=2,
                capacity=3,
                location="Indoor",
                is_active=True,
                restaurant_id=restaurant.id
            )
            session.add(table)
            await session.commit()
            await session.refresh(table)
            return (restaurant.id,table.id)
    return asyncio.run(insert())

@pytest.fixture(scope="function")
def client(insert_users):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def get_token_admin(client):
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
    form_data = {
        'username': 'test@gmail.com',
        'password': 'password'
    }
    response = client.post("/auth/log_in", data=form_data)
    token = response.json().get("access_token")
    return token