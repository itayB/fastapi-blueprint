import asyncio
import logging

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from app.db import Base
from app.settings import Settings

logging.basicConfig(level=logging.INFO, format="%(levelname)s [%(name)s] %(message)s")


def database_url() -> str:
    url = Settings().database_url
    if url is None:
        raise RuntimeError("DATABASE_URL is not set")
    return str(url)


def run_migrations_offline() -> None:
    context.configure(
        url=database_url(),
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    engine = create_async_engine(database_url(), poolclass=pool.NullPool)
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
