from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Request
from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def open_session_factory(
    database_url: PostgresDsn | None,
) -> AsyncIterator[async_sessionmaker[AsyncSession] | None]:
    if database_url is None:
        yield None
        return
    engine = create_async_engine(str(database_url), pool_pre_ping=True)
    try:
        yield async_sessionmaker(engine, expire_on_commit=False)
    finally:
        await engine.dispose()


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    session_factory: async_sessionmaker[AsyncSession] | None = getattr(
        request.state, "session_factory", None
    )
    if session_factory is None:
        raise RuntimeError("DATABASE_URL is not set")
    async with session_factory() as session:
        yield session
