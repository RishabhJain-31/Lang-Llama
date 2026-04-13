from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    """Simple uptime endpoint to verify API server status."""
    return {"status": "ok"}
