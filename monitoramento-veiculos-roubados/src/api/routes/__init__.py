from fastapi import APIRouter

router = APIRouter()

from .health import router as health_router
from .alerts import router as alerts_router
from .monuv_webhooks import router as monuv_webhooks_router

router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(alerts_router, prefix="/alerts", tags=["alerts"])
router.include_router(monuv_webhooks_router, prefix="/monuv", tags=["monuv"])