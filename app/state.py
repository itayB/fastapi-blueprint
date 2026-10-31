from asyncio import Event
from typing import TypedDict

from fastapi import Request


class AppState(TypedDict):
    readiness_event: Event


def get_readiness_event(request: Request) -> Event | None:
    return getattr(request.state, "readiness_event", None)
