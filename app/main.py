from asyncio import Event
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import partial

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from app.db import open_session_factory
from app.routes import health
from app.settings import Settings
from app.state import AppState


@asynccontextmanager
async def lifespan(app: FastAPI, settings: Settings) -> AsyncIterator[AppState]:
    async with open_session_factory(settings.database_url) as session_factory:
        readiness_event = Event()
        readiness_event.set()
        yield {"readiness_event": readiness_event, "session_factory": session_factory}


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    app = FastAPI(
        title=settings.project_name, lifespan=partial(lifespan, settings=settings)
    )
    app.add_middleware(GZipMiddleware, minimum_size=1_000)
    app.include_router(health.router, prefix="/v1")
    return app


app = create_app()
