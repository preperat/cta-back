#!/bin/bash
# Comprehensive test runner script

echo "=== Checking code quality ==="
flake8 app tests || echo "Code quality issues found, but continuing tests..."

echo "=== Running Unit Tests ==="
PYTHONPATH=. python -m unittest discover -s tests

echo -e "\n=== Running API Tests with HTTPie ==="
./tests/test_api.py

echo -e "\n=== Running Simple Tests with pytest ==="
PYTHONPATH=. pytest -xvs tests/test_basic.py tests/test_conversations.py tests/test_fastapi.py tests/test_simple_unittest.py tests/test_unittest.py

echo -e "\n=== Running Database Tests ==="
./scripts/test_db_operations.py

echo -e "\nAll tests completed!"
