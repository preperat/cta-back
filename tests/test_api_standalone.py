#!/usr/bin/env python
"""
Standalone API Test Script using HTTPie

This script tests the API endpoints
without any dependencies on pytest.
Run with: ./tests/test_api_standalone.py
"""

import json
import os
import subprocess
import sys
import time

# API configuration
API_V1_STR = "/api/v1"
BASE_URL = f"http://localhost:8000{API_V1_STR}"


def run_command(command):
    """Run a shell command and return the parsed JSON response."""
    print(f"\n> {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Command failed: {result.stderr}")
        return None

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"❌ Failed to parse JSON response: {result.stdout}")
        return None


def test_api():
    """Test the entire API workflow."""
    print("\n=== Testing API Workflow ===")

    # 1. Create a conversation
    print("\n1. Creating a conversation...")
    response = run_command(
        f'http POST {BASE_URL}/conversations/ title="Standalone Test Conversation"'
    )
    if not response or "id" not in response:
        print("❌ Failed to create conversation")
        return False

    conversation_id = response["id"]
    print(f"✅ Created conversation with ID: {conversation_id}")

    # 2. Get all conversations
    print("\n2. Getting all conversations...")
    response = run_command(f"http GET {BASE_URL}/conversations/")
    if not response or not isinstance(response, list):
        print("❌ Failed to get conversations")
        return False

    print(f"✅ Retrieved {len(response)} conversations")

    # 3. Get specific conversation
    print(f"\n3. Getting conversation {conversation_id}...")
    response = run_command(f"http GET {BASE_URL}/conversations/{conversation_id}")
    if not response or "id" not in response or response["id"] != conversation_id:
        print(f"❌ Failed to get conversation {conversation_id}")
        return False

    print(f"✅ Retrieved conversation {conversation_id}")

    # 4. Update conversation
    print(f"\n4. Updating conversation {conversation_id}...")
    response = run_command(
        f'http PUT {BASE_URL}/conversations/{conversation_id} title="Updatd Standalone"'
    )
    if (
        not response
        or "id" not in response
        or response["title"] != "Updated Standalone Test Conversation"
    ):
        print(f"❌ Failed to update conversation {conversation_id}")
        return False

    print(f"✅ Updated conversation {conversation_id}")

    # 5. Create message
    print(f"\n5. Creating message in conversation {conversation_id}...")
    response = run_command(
        f"http POST {BASE_URL}/conversations/{conversation_id}/messages "
        f'content="This is a test message from standalone script" '
        f"message_type=user conversation_id:={conversation_id}"
    )
    if not response or "id" not in response:
        print("❌ Failed to create message")
        return False

    message_id = response["id"]
    print(f"✅ Created message with ID: {message_id}")

    # 6. Wait for AI response and get messages
    print("\n6. Waiting for AI response...")
    time.sleep(2)

    print(
        f"✅ Created message with ID: {message_id} in conversation {conversation_id}. "
        "Waiting for AI response..."
    )

    print(f"\n7. Getting messages for conversation {conversation_id}...")
    response = run_command(
        f"http GET {BASE_URL}/conversations/{conversation_id}/messages"
    )
    if not response or not isinstance(response, list) or len(response) == 0:
        print(f"❌ Failed to get messages for conversation {conversation_id}")
        return False

    print(f"✅ Retrieved {len(response)} messages")

    # Check message types
    message_types = [
        msg.get("message_type") for msg in response if "message_type" in msg
    ]
    print(f"Message types found: {message_types}")

    if "user" in message_types:
        print("✅ Found user messages")
    else:
        print("⚠️ No user messages found")

    if "ai" in message_types:
        print("✅ Found AI messages")
    else:
        print("⚠️ No AI messages found yet (might need more time)")

    print("\n=== API Test Completed Successfully ===")
    return True


if __name__ == "__main__":
    # Make sure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(script_dir))  # Change to parent directory (back/)

    # Run the test
    success = test_api()
    sys.exit(0 if success else 1)
