import pytest
from fastapi.testclient import TestClient

# Mark the test module as using asyncio
pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_create_conversation(client):
    """Test creating a new conversation."""
    response = client.post(
        "/conversations/",
        json={"title": "Test Conversation"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Conversation"

@pytest.mark.asyncio
async def test_get_conversations(client):
    """Test getting all conversations."""
    # First create a conversation
    client.post(
        "/conversations/",
        json={"title": "Test Conversation for List"}
    )
    
    # Then get all conversations
    response = client.get("/conversations/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0 