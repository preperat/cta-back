#!/usr/bin/env python
"""
API Test Suite using pytest and HTTPie

This module contains pytest tests for the API endpoints.
Run with: python tests/test_api_pytest.py
"""

import json
import subprocess
import sys
import time
from typing import Any, Dict

# API configuration
API_V1_STR = "/api/v1"
BASE_URL = f"http://localhost:8000{API_V1_STR}"

# Global variable to store conversation ID between tests
CONVERSATION_ID = None
MESSAGE_ID = None


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


def test_01_create_conversation():
    """Test creating a conversation."""
    global CONVERSATION_ID

    command = f'http POST {BASE_URL}/conversations/ title="Pytest Test Conversation"'
    response = run_command(command)

    assert "id" in response, "Failed to create conversation"
    CONVERSATION_ID = response["id"]
    print(f"✅ Created conversation with ID: {CONVERSATION_ID}")


def test_02_get_conversations():
    """Test getting all conversations."""
    command = f"http GET {BASE_URL}/conversations/"
    response = run_command(command)

    assert isinstance(response, list), "Response should be a list"
    assert len(response) > 0, "Should have at least one conversation"
    print(f"✅ Retrieved {len(response)} conversations")


def test_03_get_conversation():
    """Test getting a specific conversation."""
    global CONVERSATION_ID
    assert CONVERSATION_ID is not None, "Conversation ID not set"

    command = f"http GET {BASE_URL}/conversations/{CONVERSATION_ID}"
    response = run_command(command)

    assert "id" in response, "Response should contain id"
    assert response["id"] == CONVERSATION_ID, "ID should match"
    assert "title" in response, "Response should contain title"
    print(f"✅ Retrieved conversation {CONVERSATION_ID}")


def test_04_update_conversation():
    """Test updating a conversation."""
    global CONVERSATION_ID
    assert CONVERSATION_ID is not None, "Conversation ID not set"

    command = (
        f"http PUT {BASE_URL}/conversations/{CONVERSATION_ID} "
        f'title="Updated Pytest Test Conversation"'
    )
    response = run_command(command)  # Run the command

    assert "id" in response, "Response should contain id"
    assert response["id"] == CONVERSATION_ID, "ID should match"
    assert "title" in response, "Response should contain title"
    assert (
        response["title"] == "Updated Pytest Test Conversation"
    ), "Title should be updated"
    print(f"✅ Updated conversation {CONVERSATION_ID}")


def test_05_create_message():
    """Test creating a message."""
    global CONVERSATION_ID, MESSAGE_ID
    assert CONVERSATION_ID is not None, "Conversation ID not set"

    command = (
        f"http POST {BASE_URL}/conversations/{CONVERSATION_ID}/messages "
        f'content="This is a test message from pytest" '
        f"message_type=user conversation_id={CONVERSATION_ID}"
    )
    response = run_command(command)

    assert "id" in response, "Response should contain id"
    assert "content" in response, "Response should contain content"
    assert "message_type" in response, "Response should contain message_type"
    assert (
        response["conversation_id"] == CONVERSATION_ID
    ), "Conversation ID should match"

    MESSAGE_ID = response["id"]
    print(
        f"✅ Created message with ID: {MESSAGE_ID} in conversation {CONVERSATION_ID}. "
        "AI will respond asynchronously."
    )


def test_06_get_messages():
    """Test getting all messages for a conversation."""
    global CONVERSATION_ID
    assert CONVERSATION_ID is not None, "Conversation ID not set"

    # Wait a moment for the background AI response to be generated
    time.sleep(2)

    command = f"http GET {BASE_URL}/conversations/{CONVERSATION_ID}/messages"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    assert result.returncode == 0, f"Command failed: {result.stderr}"

    try:
        response = json.loads(result.stdout)

        assert isinstance(response, list), "Response should be a list"
        assert len(response) > 0, "Should have at least one message"

        # Check if we have both user and AI messages
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

    except json.JSONDecodeError:
        assert False, f"Failed to parse JSON response: {result.stdout}"


def run_tests():
    """Run all tests in sequence."""
    tests = [
        test_01_create_conversation,
        test_02_get_conversations,
        test_03_get_conversation,
        test_04_update_conversation,
        test_05_create_message,
        test_06_get_messages,
    ]

    success = True
    for test in tests:
        try:
            print(f"\n=== Running {test.__name__} ===")
            test()
            print(f"✅ {test.__name__} passed")
        except AssertionError as e:
            print(f"❌ {test.__name__} failed: {e}")
            success = False
            break

    return success


if __name__ == "__main__":
    print("Running API tests...")
    success = run_tests()
    print("\n=== Test Summary ===")
    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Tests failed!")
        sys.exit(1)
