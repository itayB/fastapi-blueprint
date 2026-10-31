from asyncio import Event
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.models.health import Liveness, Readiness
from app.state import get_readiness_event

router = APIRouter(tags=["health"])


@router.get("/liveness")
def liveness() -> Liveness:
    """Liveness probe."""
    return Liveness()


@router.get(
    "/readiness",
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": Readiness}},
)
def readiness(
    response: Response,
    readiness_event: Annotated[Event | None, Depends(get_readiness_event)],
) -> Readiness:
    """Readiness probe."""
    if readiness_event is None or not readiness_event.is_set():
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return Readiness(status="unavailable")
    return Readiness(status="ok")
