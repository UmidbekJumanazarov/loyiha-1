from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from order_service.infrastructure.db_models import Base

# SQLite (aiosqlite orqali async)
DATABASE_URL = "sqlite+aiosqlite:///./orders.db"

engine = create_async_engine(DATABASE_URL, echo=False)
SessionFactory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    """Jadvalarni yaratadi (startup vaqtida chaqiriladi)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)