"""Ponto de entrada da aplicação FastAPI."""

from typing import Any

from fastapi import FastAPI, HTTPException

from app.api.health import router as health_router
from app.schemas.telemetry import TelemetryPayload
from app.services.telemetry_validation import InvalidTelemetryError, validate_telemetry

app = FastAPI(title="Backend da Estação Meteorológica", version="0.1.0")
app.include_router(health_router)


@app.post("/api/v1/telemetry/validate", response_model=TelemetryPayload)
def validate_payload(payload: dict[str, Any]) -> TelemetryPayload:
    """Valida uma mensagem sem persistir; a ingestão MQTT será adicionada depois."""
    try:
        return validate_telemetry(payload)
    except InvalidTelemetryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
