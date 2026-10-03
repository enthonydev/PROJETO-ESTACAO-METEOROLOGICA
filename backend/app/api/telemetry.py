"""Endpoint HTTP opcional de apoio para integração sem o transporte MQTT."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_measurement_repository
from app.core.config import settings
from app.repositories.measurements import MeasurementRepository
from app.schemas.telemetry import TelemetryPayload
from app.services.telemetry_validation import InvalidTelemetryError, validate_telemetry


router = APIRouter(prefix="/api/v1/telemetry", tags=["telemetry"])


@router.post("", response_model=TelemetryPayload, status_code=status.HTTP_201_CREATED)
def ingest_telemetry(
    payload: dict[str, Any],
    repository: MeasurementRepository = Depends(get_measurement_repository),
) -> TelemetryPayload:
    """Valida e persiste telemetria somente quando o modo de apoio está habilitado.

    O endpoint não substitui o MQTT como transporte principal da arquitetura.
    """
    if not settings.enable_http_ingestion:
        raise HTTPException(status_code=404, detail="Endpoint de ingestão HTTP desabilitado")

    try:
        validated = validate_telemetry(payload)
    except InvalidTelemetryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    repository.add(validated)
    return validated
