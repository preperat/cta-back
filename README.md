# Claytons Travel Assistant - Backend

A FastAPI-based backend for the Claytons Travel Assistant application, featuring AI-powered conversation capabilities with vector search and PostgreSQL database.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL 15+ with pgvector extension
- Docker and Docker Compose (optional, for containerized database)

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cta/back
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development tools
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Database Setup

1. **Start PostgreSQL with Docker**
   ```bash
   docker-compose up -d
   ```

2. **Apply database migrations**
   ```bash
   alembic upgrade head
   ```

3. **Verify database connection**
   ```bash
   python db_test.py
   ```

## 🧪 Testing

### Database Testing

The project includes scripts to test database functionality:

1. **Test database connection**
   ```bash
   python db_test.py
   ```
   This verifies connectivity to both the PostgreSQL superuser and application user accounts.

2. **Test database operations**
   ```bash
   ./scripts/test_db_operations.py
   ```
   This script tests:
   - Creating conversations and messages
   - Retrieving conversations with their related messages
   - Verifying relationships between models

   The script demonstrates proper usage of SQLAlchemy async patterns, including:
   - Using `selectinload` to explicitly load relationships
   - Proper session management with async context managers
   - Error handling in async operations

### Running API Tests

```bash
pytest
```

## 🛠️ Development

### Project Structure

```
back/
├── alembic/              # Database migrations
├── app/                  # Application code
│   ├── api/              # API endpoints
│   ├── core/             # Core functionality
│   ├── db/               # Database setup
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── services/         # Business logic
├── scripts/              # Utility scripts
└── tests/                # Test suite
```

### Key Components

- **FastAPI**: Web framework for building APIs
- **SQLAlchemy**: ORM for database interactions
- **Alembic**: Database migration tool
- **Pydantic**: Data validation and settings management
- **Anthropic Claude**: AI model for conversation generation
- **pgvector**: PostgreSQL extension for vector similarity search

### Adding New Features

1. Create or update SQLAlchemy models in `app/models/`
2. Generate migrations with `alembic revision --autogenerate -m "Description"`
3. Create Pydantic schemas in `app/schemas/`
4. Implement API endpoints in `app/api/endpoints/`
5. Add tests for new functionality

## 📚 Documentation

API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## 📝 License

[Specify your license] 