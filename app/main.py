from fastapi import FastAPI

from app.routes import health
from app.settings import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    app = FastAPI(title=settings.project_name)
    app.include_router(health.router, prefix="/v1")
    return app


app = create_app()
