import asyncio
from typing import Annotated

import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session, open_session_factory
from app.main import create_app
from app.settings import Settings

DATABASE_URL = PostgresDsn("postgresql+asyncpg://user:pass@db.invalid:5432/app")


async def open_and_inspect(database_url: PostgresDsn | None) -> object:
    async with open_session_factory(database_url) as session_factory:
        if session_factory is None:
            return None
        return session_factory.kw["bind"].url.drivername


def test_no_session_factory_without_database_url() -> None:
    assert asyncio.run(open_and_inspect(None)) is None


def test_session_factory_uses_asyncpg_without_connecting() -> None:
    assert asyncio.run(open_and_inspect(DATABASE_URL)) == "postgresql+asyncpg"


def test_settings_read_database_url_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", str(DATABASE_URL))

    assert Settings(_env_file=None).database_url == DATABASE_URL


def test_get_session_fails_loudly_without_database_url() -> None:
    app = create_app(Settings(_env_file=None, database_url=None))

    @app.get("/needs-db")
    def needs_db(session: Annotated[AsyncSession, Depends(get_session)]) -> None:
        pass

    with TestClient(app) as client, pytest.raises(RuntimeError, match="DATABASE_URL"):
        client.get("/needs-db")
