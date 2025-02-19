import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/users/",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpass123"
            }
        )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com" 