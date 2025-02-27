#!/usr/bin/env python
"""
Simple API Test Script using HTTPie and pytest

This script tests the API endpoints using HTTPie commands.
Run with: python -m pytest tests/test_api_simple.py -v
"""

import json
import subprocess
import sys
import time

# API configuration
API_V1_STR = "/api/v1"
BASE_URL = f"http://localhost:8000{API_V1_STR}"


def test_api_workflow():
    """Test the entire API workflow in a single test."""
    print("\nTesting API workflow...")

    # 1. Create a conversation
    cmd = f'http POST {BASE_URL}/conversations/ title="Simple Test Conversation"'
    print(f"\n> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to create conversation: {result.stderr}"

    response = json.loads(result.stdout)
    conversation_id = response["id"]
    assert conversation_id > 0, "Invalid conversation ID"
    print(f"✅ Created conversation with ID: {conversation_id}")

    # 2. Get all conversations
    cmd = f"http GET {BASE_URL}/conversations/"
    print(f"\n> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to get conversations: {result.stderr}"

    response = json.loads(result.stdout)
    assert isinstance(response, list), "Response should be a list"
    assert len(response) > 0, "Should have at least one conversation"
    print(f"✅ Retrieved {len(response)} conversations")

    # 3. Get specific conversation
    cmd = f"http GET {BASE_URL}/conversations/{conversation_id}"
    print(f"\n> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to get conversation: {result.stderr}"

    response = json.loads(result.stdout)
    assert response["id"] == conversation_id, "ID should match"
    print(f"✅ Retrieved conversation {conversation_id}")

    # 4. Update conversation
    cmd = (
        f"http PUT {BASE_URL}/conversations/{conversation_id} "
        f'title="Updated Simple Test Conversation"'
    )
    print(f"\n> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to update conversation: {result.stderr}"

    response = json.loads(result.stdout)
    assert response["id"] == conversation_id, "ID should match"
    assert (
        response["title"] == "Updated Simple Test Conversation"
    ), "Title should be updated"
    print(f"✅ Updated conversation {conversation_id}")

    # 5. Create message
    cmd = (
        f"http POST {BASE_URL}/conversations/{conversation_id}/messages "
        f'content="This is a test message" '
        f"message_type=user conversation_id:={conversation_id}"
    )
    print(f"\n> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to create message: {result.stderr}"

    response = json.loads(result.stdout)
    message_id = response["id"]
    assert message_id > 0, "Invalid message ID"
    print(f"✅ Created message with ID: {message_id}")

    # 6. Wait for AI response and get messages
    print(
        f"✅ Created message in conversation {conversation_id}. "
        "Waiting for AI response..."
    )
    time.sleep(2)

    cmd = f"http GET {BASE_URL}/conversations/{conversation_id}/messages"
    print(f"\n> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to get messages: {result.stderr}"

    response = json.loads(result.stdout)
    assert isinstance(response, list), "Response should be a list"
    assert len(response) > 0, "Should have at least one message"

    message_types = [
        msg.get("message_type") for msg in response if "message_type" in msg
    ]
    print(f"Message types found: {message_types}")

    assert "user" in message_types, "Should have user messages"
    print("✅ Found user messages")

    if "ai" in message_types:
        print("✅ Found AI messages")
    else:
        print("⚠️ No AI messages found yet (might need more time)")

    print("\nAPI workflow test completed successfully!")


if __name__ == "__main__":
    # Run the test directly
    import pytest

    sys.exit(pytest.main(["-xvs", __file__]))
