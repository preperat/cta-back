import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_async_session
from app.models.base import Base

# Test database URL - using SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture
async def async_engine():
    """Create a test async engine"""
    engine = create_async_engine(TEST_DATABASE_URL)
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Cleanup
    await engine.dispose()

@pytest.fixture
async def async_session(async_engine):
    """Create a test async session"""
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

@pytest.fixture
def test_client(async_session):
    """Create a test client with a test database session"""
    async def override_get_session():
        yield async_session

    app.dependency_overrides[get_async_session] = override_get_session
    return TestClient(app) 