from app.core.config import settings
from app.models.conversation import Conversation


def test_create_conversation():
    """Test creating a conversation model."""
    conversation = Conversation(title="Test Conversation")
    assert conversation.title == "Test Conversation"


def test_get_conversation():
    """Test conversation model properties."""
    conversation = Conversation(title="Test Conversation")
    assert conversation.id is None  # ID is None until saved to DB


def test_get_conversations(client):
    """Test getting all conversations endpoint exists."""
    # Get the API prefix from settings
    api_prefix = settings.API_V1_STR

    # Just test that the endpoint exists and returns a 200 status code
    response = client.get(f"{api_prefix}/conversations/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
