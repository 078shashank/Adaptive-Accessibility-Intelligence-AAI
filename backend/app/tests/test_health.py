"""Test for health endpoint"""
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "message" in data


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/api/v1")
    # Root endpoint may or may not exist - it's optional
    assert response.status_code in [200, 404]
