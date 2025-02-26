import pytest

def test_simple():
    """A simple test that should always pass."""
    assert True

def test_app_root(client):
    """Test that the app root returns a 200 status code."""
    response = client.get("/")
    assert response.status_code == 200 