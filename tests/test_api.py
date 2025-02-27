#!/usr/bin/env python
"""
API Test Script using HTTPie

This script tests the API endpoints using HTTPie commands.
Run this script to verify that all API endpoints are working correctly.

Requirements:
- HTTPie installed (pip install httpie)
- API server running (uvicorn app.main:app --reload)
"""

import json
import subprocess
import sys
import time
from typing import Any, Dict, Optional

# Update this to match your API prefix
API_V1_STR = "/api/v1"  # This should match settings.API_V1_STR
BASE_URL = f"http://localhost:8000{API_V1_STR}"


def run_command(command: str) -> Dict[str, Any]:
    """Run a shell command and return the parsed JSON response."""
    print(f"\n> {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return {}

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Error parsing JSON: {result.stdout}")
        return {}


def test_create_conversation() -> Optional[int]:
    """Test creating a conversation."""
    print("\n=== Testing Create Conversation ===")
    command = f'http POST {BASE_URL}/conversations/ title="HTTPie Test Conversation"'
    response = run_command(command)

    if "id" in response:
        print(f"✅ Created conversation with ID: {response['id']}")
        return response["id"]
    else:
        print("❌ Failed to create conversation")
        return None


def test_get_conversations() -> None:
    """Test getting all conversations."""
    print("\n=== Testing Get All Conversations ===")
    command = f"http GET {BASE_URL}/conversations/"
    response = run_command(command)

    if isinstance(response, list):
        print(f"✅ Retrieved {len(response)} conversations")
    else:
        print("❌ Failed to retrieve conversations")


def test_get_conversation(conversation_id: int) -> None:
    """Test getting a specific conversation."""
    print(f"\n=== Testing Get Conversation {conversation_id} ===")
    command = f"http GET {BASE_URL}/conversations/{conversation_id}"
    response = run_command(command)

    if "id" in response and response["id"] == conversation_id:
        print(f"✅ Retrieved conversation {conversation_id}")
    else:
        print(f"❌ Failed to retrieve conversation {conversation_id}")


def test_update_conversation(conversation_id: int) -> None:
    """Test updating a conversation."""
    print(f"\n=== Testing Update Conversation {conversation_id} ===")
    command = (
        f"http PUT {BASE_URL}/conversations/{conversation_id} "
        f'title="Updated HTTPie Test Conversation"'
    )
    response = run_command(command)

    if "id" in response and response["title"] == "Updated HTTPie Test Conversation":
        print(f"✅ Updated conversation {conversation_id}")
    else:
        print(f"❌ Failed to update conversation {conversation_id}")


def test_create_message(conversation_id: int) -> Optional[int]:
    """Test creating a message."""
    print(f"\n=== Testing Create Message in Conversation {conversation_id} ===")
    command = (
        f"http POST {BASE_URL}/conversations/{conversation_id}/messages "
        f'content="This is a test message from HTTPie" '
        f"message_type=user conversation_id:={conversation_id}"
    )
    response = run_command(command)

    assert "id" in response, "Response should contain id"
    assert "content" in response, "Response should contain content"
    assert "message_type" in response, "Response should contain message_type"
    assert (
        response["conversation_id"] == conversation_id
    ), "Conversation ID should match"

    MESSAGE_ID = response["id"]
    print(
        f"✅ Created message with ID: {MESSAGE_ID} in conversation {conversation_id}. "
        "AI will respond asynchronously."
    )
    return MESSAGE_ID


def test_get_messages(conversation_id: int) -> None:
    """Test getting all messages for a conversation."""
    print(f"\n=== Testing Get Messages for Conversation {conversation_id} ===")
    # Wait a moment for the background AI response to be generated
    time.sleep(2)

    command = f"http GET {BASE_URL}/conversations/{conversation_id}/messages"

    # Run the command and capture the full output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Command failed with error: {result.stderr}")
        return

    try:
        response = json.loads(result.stdout)

        if isinstance(response, list):
            print(f"✅ Retrieved {len(response)} messages")
            if response and len(response) > 0:
                print(f"First message: {json.dumps(response[0], indent=2)}")
        else:
            print(f"❌ Response is not a list: {response}")
            return

        # Check if we have both user and AI messages
        message_types = [
            msg.get("message_type") for msg in response if "message_type" in msg
        ]
        print(f"Message types found: {message_types}")

        if "user" in message_types:
            print("✅ Found user messages")
        else:
            print("⚠️ Did not find user messages")

        if "ai" in message_types:
            print("✅ Found AI messages")
        else:
            print("⚠️ Did not find AI messages")
    except json.JSONDecodeError:
        print(f"❌ Failed to parse JSON response: {result.stdout}")


def test_delete_conversation(conversation_id: int) -> None:
    """Test deleting a conversation."""
    print(f"\n=== Testing Delete Conversation {conversation_id} ===")
    command = f"http DELETE {BASE_URL}/conversations/{conversation_id}"
    response = run_command(command)

    if "success" in response and response["success"]:
        print(f"✅ Deleted conversation {conversation_id}")
    else:
        print(f"❌ Failed to delete conversation {conversation_id}")


def main() -> None:
    """Run all tests."""
    print("Starting API tests with HTTPie...")

    # Test conversation endpoints
    conversation_id = test_create_conversation()
    if not conversation_id:
        print("Cannot continue tests without a valid conversation ID")
        sys.exit(1)

    test_get_conversations()
    test_get_conversation(conversation_id)
    test_update_conversation(conversation_id)

    # Test message endpoints
    message_id = test_create_message(conversation_id)
    if not message_id:
        print("Failed to create message, but continuing tests")

    test_get_messages(conversation_id)

    # Test deletion (optional - comment out if you want to keep the test data)
    # test_delete_conversation(conversation_id)

    print("\nAPI tests completed!")


if __name__ == "__main__":
    main()
