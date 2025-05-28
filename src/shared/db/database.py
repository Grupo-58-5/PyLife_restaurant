
from typing import Final
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.orm.session import Session
from src.shared.infraestructure.settings import settings

DATABASE_URL: Final = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
engine = create_engine(DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
    )
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
