# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base
from src.main import app
from fastapi.testclient import TestClient
from src.config import settings
from src.database.db import get_db

# Use the test database URL
TEST_DATABASE_URL = str(settings.DB_URL_TEST)

# Create a test database engine and session
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

# Create test database tables
@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)  # Create tables before tests
    yield
    print("teardown test db")
    Base.metadata.drop_all(bind=engine)  # Drop tables after tests

# Override `get_db` dependency
@pytest.fixture(scope="function")
def test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply the override
@pytest.fixture(scope="function")
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
