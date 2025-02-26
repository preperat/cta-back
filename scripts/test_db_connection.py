#!/usr/bin/env python
"""Script to test async database connection."""
import asyncio
import sys
from sqlalchemy import text

sys.path.append(".")  # Add current directory to path

from app.db.base import engine
from app.config import settings


async def test_async_connection():
    """Test async database connection using SQLAlchemy."""
    try:
        print(f"Testing connection to {settings.DATABASE_URL}...")
        
        async with engine.connect() as conn:
            # Run a simple query
            result = await conn.execute(text("SELECT 1"))
            data = await result.fetchone()
            
            if data and data[0] == 1:
                print("✅ Async database connection successful!")
                
                # Additional database info
                version = await conn.execute(text("SELECT version()"))
                version_str = await version.scalar()
                print(f"PostgreSQL version: {version_str}")
                
                # Test for pgvector extension
                try:
                    pgvector = await conn.execute(text("SELECT * FROM pg_extension WHERE extname = 'vector'"))
                    pgvector_exists = await pgvector.fetchone()
                    
                    if pgvector_exists:
                        print("✅ pgvector extension is installed")
                    else:
                        print("❌ pgvector extension is NOT installed")
                except Exception as e:
                    print(f"❌ Error checking pgvector: {str(e)}")
                
                return True
            else:
                print("❌ Connection test failed!")
                return False
                
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_async_connection())
    sys.exit(0 if result else 1) 