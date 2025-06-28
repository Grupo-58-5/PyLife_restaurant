from typing import AsyncGenerator, Final
from sqlmodel import StaticPool, create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.shared.config.settings import settings

# DATABASE_URL: Final = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
# engine = create_engine(DATABASE_URL,
#     echo=True,
#     pool_size=5,
#     max_overflow=10,
#     pool_timeout=30,
#     pool_recycle=1800
#     )

# def get_session():
#     with Session(engine) as session:
#         try:
#             yield session
#         finally:
#             session.close()
TESTING = settings.TESTING
DATABASE_URL: Final = f"postgresql+asyncpg://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
DATABASE_TEST = "sqlite+aiosqlite:///:memory:"

if not TESTING:
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
        future=True
    )
else:
    engine = create_async_engine(
        DATABASE_TEST,
        poolclass=StaticPool,
        future=True,
    )

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    print("Esta en testing: ",TESTING)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
