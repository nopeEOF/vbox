from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from myapp.db.tables import Base
from collections.abc import AsyncIterator
from myapp import readconfig


async def async_engine():
    """Main program function."""

    config = readconfig.get_config()
    engine = create_async_engine("sqlite+aiosqlite:///" + config["db"])

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return engine


async def session() -> AsyncIterator[AsyncSession]:
    engine = await async_engine()
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    try:
        yield async_session
    finally:
        await engine.dispose()
