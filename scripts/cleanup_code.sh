#!/bin/bash
# Script to clean up code style issues

echo "=== Running isort to sort imports ==="
isort app/ tests/

echo "=== Running black to format code ==="
black app/ tests/

echo "=== Running flake8 to check for remaining issues ==="
flake8 app/ tests/

echo "=== Done ==="
