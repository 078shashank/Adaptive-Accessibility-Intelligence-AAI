"""Pytest Configuration and Fixtures"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import User, AccessibilityProfile
from app.services.auth import get_password_hash


# Create test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_aai.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app, base_url="http://127.0.0.1:8000")


@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(db=next(override_get_db())):
    """Create a test user"""
    user = User(
        email="testuser@example.com",
        full_name="Test User",
        hashed_password=get_password_hash("testpassword123")
    )
    db.add(user)
    db.flush()

    # Create accessibility profile
    profile = AccessibilityProfile(user_id=user.id)
    db.add(profile)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture
def test_client():
    """Return FastAPI test client"""
    return client
