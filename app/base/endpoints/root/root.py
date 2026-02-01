from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.configs.settings import project_details, settings

router = APIRouter(tags=["Root"], include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def root(request: Request) -> Response:
    """
    Render the root landing page.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        Response: The rendered HTML template response.
    """
    project_name = project_details.get("name", "API Service")
    project_version = project_details.get("version", "0.0.0")

    return templates.TemplateResponse(
        request=request,
        name="root.html",
        context={
            "project_name": project_name,
            "project_version": project_version,
            "environment": settings.APP_ENV,
        },
    )
