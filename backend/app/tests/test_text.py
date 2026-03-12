"""Test for text simplification endpoint"""
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.fixture
def auth_token():
    """Get auth token for testing"""
    # Register and login
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "texttest@example.com",
            "password": "testpass123",
        },
    )
    
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "texttest@example.com",
            "password": "testpass123",
        },
    )
    return response.json()["access_token"]


def test_simplify_text(auth_token):
    """Test text simplification"""
    response = client.post(
        "/api/v1/text/simplify",
        json={
            "text": "The anthropomorphic characteristics of computers have long been a subject of philosophical debate among cognitive scientists and technologists alike.",
            "reading_level": "intermediate",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "simplified_text" in data
    assert "original_text" in data


def test_simplify_text_too_short(auth_token):
    """Test simplification with text too short"""
    response = client.post(
        "/api/v1/text/simplify",
        json={
            "text": "Short",
            "reading_level": "intermediate",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 400


def test_simplify_text_unauthorized():
    """Test simplification without authentication"""
    response = client.post(
        "/api/v1/text/simplify",
        json={
            "text": "Some text to simplify that is long enough",
            "reading_level": "intermediate",
        },
    )
    # Should fail or return 403 without auth
    assert response.status_code in [401, 403]
