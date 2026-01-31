from fastapi import APIRouter

from app.configs.settings import settings

from .schemas import InfoResponse

router = APIRouter(prefix="/info", tags=["System"])


@router.get("", response_model=InfoResponse)
def get_info() -> InfoResponse:
    """
    Retrieve public application information.

    Returns:
        InfoResponse: A JSON object containing the application name, version, and debug mode status.
    """
    return InfoResponse(
        name=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
    )
