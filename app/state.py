from asyncio import Event
from typing import TypedDict

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class AppState(TypedDict):
    readiness_event: Event
    session_factory: async_sessionmaker[AsyncSession] | None


def get_readiness_event(request: Request) -> Event | None:
    return getattr(request.state, "readiness_event", None)
