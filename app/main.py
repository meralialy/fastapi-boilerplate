import time
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.router import router as api_router
from app.base.router import router as base_router
from app.configs.settings import settings


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    """
    Manage the application lifespan (startup and shutdown events).

    Args:
        _app (FastAPI): The application instance.
    """
    # Startup: Logic here runs BEFORE the app starts taking requests
    yield
    # Shutdown: Logic here runs AFTER the app stops taking requests


tags_metadata = [
    {
        "name": "System",
        "description": "System health checks and application information.",
    },
    {
        "name": "v1",
        "description": "API version 1 endpoints.",
    },
]

# Determine environment settings to toggle documentation and debug modes
environment = settings.APP_ENV.lower()
is_production = environment == "production"

app = FastAPI(
    title=f"{settings.APP_NAME} ({environment})",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
    openapi_tags=tags_metadata,
    swagger_ui_parameters={"docExpansion": "none"},
    docs_url=None if is_production else "/docs",
    redoc_url=None if is_production else "/redoc",
    openapi_url=None if is_production else "/openapi.json",
)

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Enable GZip compression for responses larger than 1000 bytes
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.middleware("http")
async def log_requests(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """
    Middleware to log request processing time.

    Adds an 'X-Process-Time' header to the response indicating how long
    the server took to process the request.
    """
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"

    return response


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Custom handler for HTTP exceptions to provide structured JSON errors.

    Specifically overrides 404 Not Found to provide helpful suggestions.
    """
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": "error",
                "message": "The requested resource does not exist.",
                "path": request.url.path,
                "suggestion": "Check the API documentation at /docs",
                "available_versions": ["v1"],
            },
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


app.include_router(base_router)
app.include_router(api_router)
