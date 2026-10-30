from asyncio import Event
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes import health
from app.settings import Settings
from app.state import AppState


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[AppState]:
    readiness_event = Event()
    readiness_event.set()
    yield {"readiness_event": readiness_event}


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    app = FastAPI(title=settings.project_name, lifespan=lifespan)
    app.include_router(health.router, prefix="/v1")
    return app


app = create_app()
