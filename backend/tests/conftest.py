"""
Shared test fixtures.

Provides an isolated in-memory SQLite database and a FastAPI test client
so every test runs against a clean state.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from main import app


# In-memory SQLite for fast, isolated tests
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

test_engine = create_engine(
    SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Override the production DB dependency with a test database."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Create all tables before each test, drop them after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    """Provide a fresh test client."""
    return TestClient(app)


@pytest.fixture
def sample_asset(client):
    """Create and return a sample asset for tests that need existing data."""
    response = client.post(
        "/api/assets",
        json={
            "machineName": "Test Machine Alpha",
            "status": "RUNNING",
            "uptimePercentage": 95.0,
        },
    )
    return response.json()
