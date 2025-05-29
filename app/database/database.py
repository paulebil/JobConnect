from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

DATABASE_URL = "sqlite+aiosqlite:///./job_connect.db"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create the async session factory
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# Declare the base class for models
class Base(DeclarativeBase):
    pass

# Dependency to get an async DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
