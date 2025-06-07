import pytest
from fastapi.testclient import TestClient
from sqlmodel import StaticPool, create_engine, SQLModel, Session, inspect
from src.shared.db.database import get_session

from src.main import app

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Override de la dependencia
def get_session_override():
    with Session(engine) as session:
        print("Session de test: ",session)
        yield session

app.dependency_overrides[get_session] = get_session_override

# Ejecutado antes de cada test
@pytest.fixture(name="prepare_db")
def prepare_db():
    SQLModel.metadata.create_all(engine)

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tablas creadas:", tables)
    yield
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as test_client:
        yield test_client