# Database Configuration

From sqlalalchemy.extasync import create_async_engine
from sqlalalchemy.orm import sessionmaker
From typing import AsyncGenerator

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=3600
)
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    bind=engine, 
    class=AsyncSession,
    expire_on_commit=False
)

async def get_db() :-> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session
