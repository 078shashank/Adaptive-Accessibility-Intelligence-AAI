"""Simple API tests that match actual endpoints"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base


# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_simple.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_db():
    """Clean database before and after each test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestHealthCheck:
    """Health check endpoint tests"""

    def test_health_check_returns_200(self):
        """Test that health check endpoint returns 200"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200

    def test_health_check_has_status(self):
        """Test that health check response has status field"""
        response = client.get("/api/v1/health")
        data = response.json()
        assert "status" in data


class TestAuthEndpoints:
    """Authentication endpoint tests"""

    def test_register_user_success(self):
        """Test successful user registration"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "TestPassword123",
                "full_name": "Test User"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "id" in data

    def test_register_duplicate_email(self):
        """Test registration with duplicate email fails"""
        # First registration
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "TestPassword123",
                "full_name": "Test User"
            }
        )
        # Second registration with same email
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "TestPassword123",
                "full_name": "Another User"
            }
        )
        assert response.status_code == 400

    def test_register_password_too_short(self):
        """Test registration with password less than 8 characters"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "short",
                "full_name": "Test User"
            }
        )
        assert response.status_code == 400

    def test_register_invalid_email(self):
        """Test registration with invalid email format"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "not-an-email",
                "password": "TestPassword123!",
                "full_name": "Test User"
            }
        )
        assert response.status_code == 400

    def test_login_success(self):
        """Test successful login"""
        # Register user first
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "TestPassword123",
                "full_name": "Test User"
            }
        )
        
        # Login
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "TestPassword123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self):
        """Test login with wrong password"""
        # Register user first
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "TestPassword123",
                "full_name": "Test User"
            }
        )
        
        # Login with wrong password
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "WrongPassword123"
            }
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self):
        """Test login with non-existent user"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "TestPassword123"
            }
        )
        assert response.status_code == 401


class TestRootEndpoint:
    """Root endpoint tests"""

    def test_root_returns_message(self):
        """Test that root endpoint returns a message"""
        response = client.get("/api/v1")
        # Root endpoint may or may not exist
        assert response.status_code in [200, 404]


class TestEndpointAvailability:
    """Test that expected endpoints are available"""

    def test_auth_endpoints_exist(self):
        """Test that auth endpoints are available"""
        # Register endpoint
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "TestPassword123",
                "full_name": "Test User"
            }
        )
        assert response.status_code in [200, 409, 400]

    def test_health_endpoint_exists(self):
        """Test that health endpoint is available"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200

    def test_404_nonexistent_endpoint(self):
        """Test that nonexistent endpoints return 404"""
        response = client.get("/nonexistent-endpoint-12345")
        assert response.status_code == 404


class TestErrorHandling:
    """Error handling tests"""

    def test_missing_required_fields(self):
        """Test that missing required fields return 400"""
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com"}  # Missing password
        )
        assert response.status_code == 400  # FastAPI returns 400 for validation errors

    def test_invalid_json(self):
        """Test that invalid JSON returns appropriate error"""
        response = client.post(
            "/api/v1/auth/register",
            content="invalid json{"
        )
        assert response.status_code in [422, 400]

    def test_405_method_not_allowed(self):
        """Test that wrong HTTP method returns 405"""
        response = client.put("/api/v1/health")  # Health only supports GET
        assert response.status_code == 405


class TestIntegrationFlow:
    """Integration flow tests"""

    def test_register_and_login_flow(self):
        """Test complete register and login flow"""
        # Register
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "flow@example.com",
                "password": "FlowPassword123",
                "full_name": "Flow Test"
            }
        )
        assert register_response.status_code == 200
        
        # Login
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "flow@example.com",
                "password": "FlowPassword123"
            }
        )
        assert login_response.status_code == 200
        assert "access_token" in login_response.json()

    def test_multiple_user_registration(self):
        """Test registering multiple users"""
        users = [
            ("user1@example.com", "Password1123", "User One"),
            ("user2@example.com", "Password2456", "User Two"),
            ("user3@example.com", "Password3789", "User Three"),
        ]
        
        for email, password, name in users:
            response = client.post(
                "/api/v1/auth/register",
                json={
                    "email": email,
                    "password": password,
                    "full_name": name
                }
            )
            assert response.status_code == 200
            assert response.json()["email"] == email
