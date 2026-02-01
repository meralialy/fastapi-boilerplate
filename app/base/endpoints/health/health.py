from datetime import UTC, datetime

from fastapi import APIRouter

from .schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["System"])


@router.get("", response_model=HealthResponse)
def get_health() -> HealthResponse:
    """
    Perform a health check of the application.

    Returns:
        HealthResponse: A JSON object containing the status and current timestamp.
    """
    return HealthResponse(status="healthy", timestamp=datetime.now(tz=UTC))
