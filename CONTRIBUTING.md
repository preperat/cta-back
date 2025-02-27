# Contributing Guide

## Code Quality Standards

We use the following tools to maintain code quality:

- **flake8**: For linting and checking code style
- **black**: For automatic code formatting
- **isort**: For sorting imports

### Setting up your development environment

1. Install the development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running code quality checks

All commands should be run from the `back` directory:

```bash
# Check code style with flake8
flake8 app tests

# Format code with black
black app tests

# Sort imports with isort
isort app tests
```

### Automatic code cleanup

You can run the cleanup script to automatically fix many code style issues:

```bash
chmod +x scripts/cleanup_code.sh
./scripts/cleanup_code.sh
```

### Running tests

The project includes a comprehensive test runner script:

```bash
chmod +x run_tests.sh
./run_tests.sh
```

You can also run specific tests:

```bash
# Run all pytest tests
PYTHONPATH=. pytest -xvs

# Run a specific test file
PYTHONPATH=. pytest -xvs tests/test_conversations.py

# Run a specific test function
PYTHONPATH=. pytest -xvs tests/test_conversations.py::test_create_conversation
```
