"""Test for authentication service"""
from fastapi.testclient import TestClient
from app.main import app
from app.services.auth import verify_password, get_password_hash


client = TestClient(app)


def test_register_user():
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "testpass123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "Test User"


def test_register_duplicate_email():
    """Test registration with duplicate email"""
    # Register first user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "testpass123",
        },
    )

    # Try to register with same email
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "different123",
        },
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_success():
    """Test successful login"""
    # Register user first
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "logintest@example.com",
            "password": "correctpass123",
        },
    )
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "logintest@example.com",
            "password": "correctpass123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    """Test login with wrong password"""
    # Register user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "wrongpass@example.com",
            "password": "correctpass123",
        },
    )
    
    # Try wrong password
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrongpass@example.com",
            "password": "wrongpass123",
        },
    )
    assert response.status_code == 401


def test_login_nonexistent_user():
    """Test login with non-existent user"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "anypass123",
        },
    )
    assert response.status_code == 401


def test_password_hashing():
    """Test password hashing and verification"""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    # Should be different
    assert hashed != password
    
    # Should verify correctly
    assert verify_password(password, hashed)
    
    # Should not verify incorrect password
    assert not verify_password("wrongpassword", hashed)
