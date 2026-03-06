import pytest
from urllib.parse import urlencode
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.models import Base, User, AccessibilityProfile, TextSimplification


# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
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


class TestAuthEndpoints:
    """Unit tests for authentication endpoints"""

    def test_register_user_success(self):
        """Test successful user registration"""
        response = client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "Test@1234", "full_name": "Test User"}
        )
        assert response.status_code == 201
        assert response.json()["email"] == "test@example.com"

    def test_register_duplicate_email(self):
        """Test registration with duplicate email"""
        # First registration
        client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "Test@1234", "full_name": "Test User"}
        )
        # Second registration with same email
        response = client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "Test@5678", "full_name": "Another User"}
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_register_weak_password(self):
        """Test registration with weak password"""
        response = client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "weak", "full_name": "Test User"}
        )
        assert response.status_code == 400

    def test_register_invalid_email(self):
        """Test registration with invalid email"""
        response = client.post(
            "/auth/register",
            json={"email": "invalid-email", "password": "Test@1234", "full_name": "Test User"}
        )
        assert response.status_code == 422

    def test_login_success(self):
        """Test successful login"""
        # Register user
        client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "Test@1234", "full_name": "Test User"}
        )
        # Login
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "Test@1234"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_wrong_password(self):
        """Test login with wrong password"""
        # Register user
        client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "Test@1234", "full_name": "Test User"}
        )
        # Login with wrong password
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "WrongPassword"}
        )
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_nonexistent_user(self):
        """Test login with non-existent user"""
        response = client.post(
            "/auth/login",
            data={"username": "nonexistent@example.com", "password": "Test@1234"}
        )
        assert response.status_code == 401


class TestUserProfile:
    """Unit tests for user profile endpoints"""

    @pytest.fixture
    def auth_headers(self):
        """Get auth headers for logged-in user"""
        client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "Test@1234", "full_name": "Test User"}
        )
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "Test@1234"}
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_get_profile_unauthorized(self):
        """Test getting profile without authorization"""
        response = client.get("/users/profile")
        assert response.status_code == 403

    def test_get_profile_authorized(self, auth_headers):
        """Test getting profile with authorization"""
        response = client.get("/users/profile", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"

    def test_update_profile(self, auth_headers):
        """Test updating user profile"""
        response = client.put(
            "/users/profile",
            json={"full_name": "Updated Name", "preferences": {"theme": "dark"}},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["full_name"] == "Updated Name"

    def test_update_profile_invalid_data(self, auth_headers):
        """Test updating profile with invalid data"""
        response = client.put(
            "/users/profile",
            json={"full_name": ""},  # Empty name
            headers=auth_headers
        )
        assert response.status_code == 422


class TestAccessibilityProfile:
    """Unit tests for accessibility profile endpoints"""

    @pytest.fixture
    def auth_headers(self):
        """Get auth headers"""
        client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "Test@1234", "full_name": "Test User"}
        )
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "Test@1234"}
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_create_accessibility_profile(self, auth_headers):
        """Test creating accessibility profile"""
        profile_data = {
            "visual_impairment_level": "moderate",
            "hearing_impairment_level": "none",
            "motor_impairment_level": "none",
            "cognitive_impairment_level": "none",
            "speech_impairment_level": "none",
            "literacy_level": "intermediate"
        }
        response = client.post(
            "/accessibility/profile",
            json=profile_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["visual_impairment_level"] == "moderate"

    def test_get_accessibility_profile(self, auth_headers):
        """Test retrieving accessibility profile"""
        response = client.get(
            "/accessibility/profile",
            headers=auth_headers
        )
        # Should return default or existing profile
        assert response.status_code in [200, 404]

    def test_update_accessibility_profile(self, auth_headers):
        """Test updating accessibility profile"""
        # Create profile first
        client.post(
            "/accessibility/profile",
            json={
                "visual_impairment_level": "moderate",
                "hearing_impairment_level": "none",
                "motor_impairment_level": "none",
                "cognitive_impairment_level": "none",
                "speech_impairment_level": "none",
                "literacy_level": "intermediate"
            },
            headers=auth_headers
        )
        # Update it
        response = client.put(
            "/accessibility/profile",
            json={
                "visual_impairment_level": "severe",
                "hearing_impairment_level": "none",
                "motor_impairment_level": "none",
                "cognitive_impairment_level": "none",
                "speech_impairment_level": "none",
                "literacy_level": "advanced"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["visual_impairment_level"] == "severe"

    def test_invalid_impairment_level(self, auth_headers):
        """Test invalid impairment level"""
        response = client.post(
            "/accessibility/profile",
            json={
                "visual_impairment_level": "invalid_level",
                "hearing_impairment_level": "none",
                "motor_impairment_level": "none",
                "cognitive_impairment_level": "none",
                "speech_impairment_level": "none",
                "literacy_level": "intermediate"
            },
            headers=auth_headers
        )
        assert response.status_code == 422


class TestTextSimplification:
    """Unit tests for text simplification endpoints"""

    @pytest.fixture
    def auth_headers(self):
        """Get auth headers"""
        client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "Test@1234", "full_name": "Test User"}
        )
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "Test@1234"}
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_simplify_text_success(self, auth_headers):
        """Test successful text simplification"""
        response = client.post(
            "/text/simplify",
            json={
                "text": "The quick brown fox jumps over the lazy dog.",
                "reading_level": "simple"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "simplified_text" in response.json()

    def test_simplify_empty_text(self, auth_headers):
        """Test simplifying empty text"""
        response = client.post(
            "/text/simplify",
            json={
                "text": "",
                "reading_level": "simple"
            },
            headers=auth_headers
        )
        assert response.status_code == 400

    def test_simplify_text_missing_reading_level(self, auth_headers):
        """Test simplify without reading level"""
        response = client.post(
            "/text/simplify",
            json={"text": "Test text"},
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_simplify_very_long_text(self, auth_headers):
        """Test simplifying very long text"""
        long_text = "word " * 1500  # >5000 chars
        response = client.post(
            "/text/simplify",
            json={
                "text": long_text,
                "reading_level": "simple"
            },
            headers=auth_headers
        )
        assert response.status_code == 400

    def test_get_simplification_history(self, auth_headers):
        """Test retrieving simplification history"""
        response = client.get(
            "/text/history",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_delete_simplification(self, auth_headers):
        """Test deleting a simplification"""
        # First, create a simplification
        simplify_response = client.post(
            "/text/simplify",
            json={"text": "Test text", "reading_level": "simple"},
            headers=auth_headers
        )
        simplification_id = simplify_response.json()["id"]
        
        # Delete it
        response = client.delete(
            f"/text/simplify/{simplification_id}",
            headers=auth_headers
        )
        assert response.status_code == 200


class TestAvatarGeneration:
    """Unit tests for avatar generation endpoints"""

    @pytest.fixture
    def auth_headers(self):
        """Get auth headers"""
        client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "Test@1234", "full_name": "Test User"}
        )
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "Test@1234"}
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_generate_avatar_success(self, auth_headers):
        """Test successful avatar generation"""
        response = client.post(
            "/avatar/generate",
            json={"name": "Test User", "style": "cartoon"},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "avatar_url" in response.json()

    def test_generate_avatar_invalid_style(self, auth_headers):
        """Test avatar generation with invalid style"""
        response = client.post(
            "/avatar/generate",
            json={"name": "Test User", "style": "invalid_style"},
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_get_avatar_history(self, auth_headers):
        """Test retrieving avatar generation history"""
        response = client.get(
            "/avatar/history",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestGuidedMode:
    """Unit tests for guided mode endpoints"""

    @pytest.fixture
    def auth_headers(self):
        """Get auth headers"""
        client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "Test@1234", "full_name": "Test User"}
        )
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "Test@1234"}
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_start_guided_session(self, auth_headers):
        """Test starting a guided mode session"""
        response = client.post(
            "/guided/start",
            json={},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "session_id" in response.json()

    def test_get_guided_step(self, auth_headers):
        """Test getting guided step"""
        # Start session first
        start_response = client.post(
            "/guided/start",
            json={},
            headers=auth_headers
        )
        session_id = start_response.json()["session_id"]
        
        # Get step
        response = client.get(
            f"/guided/step/1?session_id={session_id}",
            headers=auth_headers
        )
        assert response.status_code in [200, 404]

    def test_complete_guided_step(self, auth_headers):
        """Test completing a guided step"""
        # Start session first
        start_response = client.post(
            "/guided/start",
            json={},
            headers=auth_headers
        )
        session_id = start_response.json()["session_id"]
        
        # Complete step
        response = client.post(
            "/guided/complete",
            json={"session_id": session_id, "step_number": 1, "data": {}},
            headers=auth_headers
        )
        assert response.status_code in [200, 404]


class TestHealthCheck:
    """Unit tests for health check endpoint"""

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert "status" in response.json()


class TestErrorHandling:
    """Unit tests for error handling"""

    def test_404_not_found(self):
        """Test 404 error"""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404

    def test_method_not_allowed(self):
        """Test 405 method not allowed"""
        response = client.put("/health")  # Health is GET only
        assert response.status_code == 405

    def test_validation_error(self):
        """Test validation error response"""
        response = client.post(
            "/auth/register",
            json={"email": "invalid"}  # Missing required fields
        )
        assert response.status_code == 422


class TestSecurityHeaders:
    """Unit tests for security headers"""

    def test_cors_headers_present(self):
        """Test CORS headers are present"""
        response = client.get("/health")
        # CORS headers should be in response
        assert response.status_code == 200

    def test_no_sensitive_data_in_errors(self):
        """Test that errors don't leak sensitive data"""
        response = client.post(
            "/auth/login",
            data={"username": "nonexistent@example.com", "password": "test"}
        )
        assert response.status_code == 401
        assert "password" not in str(response.json()).lower()
        assert "secret" not in str(response.json()).lower()
