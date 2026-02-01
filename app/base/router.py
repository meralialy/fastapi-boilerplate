from fastapi import APIRouter

from app.base.endpoints.health import health
from app.base.endpoints.info import info
from app.base.endpoints.root import root

router = APIRouter()

router.include_router(health.router)
router.include_router(info.router)
router.include_router(root.router)
