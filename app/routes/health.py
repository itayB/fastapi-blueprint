from fastapi import APIRouter

from app.models.health import Liveness

router = APIRouter(tags=["health"])


@router.get("/liveness")
def liveness() -> Liveness:
    """Liveness probe."""
    return Liveness()
