from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Async database engine
async_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    echo=settings.DEBUG  # Log SQL statements in debug mode
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    async_engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

async def get_async_session() -> AsyncSession:
    """
    Dependency for getting an async database session
    
    Yields:
        AsyncSession: Database session for async operations
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 