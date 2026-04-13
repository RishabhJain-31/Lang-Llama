from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.chat import router as chat_router

# Central v1 router: keep endpoint registration in one place.
api_router = APIRouter()

# Health check route -> GET /api/v1/health
api_router.include_router(health_router, tags=["health"])

# Chat routes -> POST /api/v1/chat
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
