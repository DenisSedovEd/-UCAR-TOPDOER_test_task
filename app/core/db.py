from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

async_engine: AsyncEngine = create_async_engine(
    settings.db.url,
    echo=settings.db.echo,
    future=settings.db.future,
)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
