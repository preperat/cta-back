"""
Configuration file for pytest.
This file is automatically recognized by pytest and used for configuration.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the app."""
    return TestClient(app)


def pytest_ignore_collect(path, config):
    """
    Return True to prevent pytest from collecting a file as a test module.
    """
    # Exclude specific test files that are meant to be run directly
    excluded_files = [
        "test_api.py",
        "test_api_simple.py",
        "test_api_pytest.py",
        "test_api_standalone.py",
    ]

    # Check if the path contains any of the excluded files
    return any(excluded in str(path) for excluded in excluded_files)
