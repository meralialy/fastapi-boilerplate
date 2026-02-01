from fastapi import APIRouter

from app.api.v1.endpoints.example import example

router = APIRouter()

router.include_router(example.router)
