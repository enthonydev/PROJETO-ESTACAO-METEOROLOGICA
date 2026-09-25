"""Endpoint de diagnóstico da aplicação."""

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.telemetry import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Indica que o processo da aplicação está ativo."""
    return HealthResponse(status="ok", service=settings.app_name)
