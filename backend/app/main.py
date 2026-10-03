"""Ponto de entrada da aplicação FastAPI."""

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.health import router as health_router
from app.api.stations import router as stations_router
from app.api.telemetry import router as telemetry_router
from app.schemas.telemetry import TelemetryPayload
from app.services.telemetry_validation import InvalidTelemetryError, validate_telemetry


app = FastAPI(title="Backend da Estação Meteorológica", version="0.2.0")
app.include_router(health_router)
app.include_router(stations_router)
app.include_router(telemetry_router)


@app.post("/api/v1/telemetry/validate", response_model=TelemetryPayload)
def validate_payload(payload: dict[str, Any]) -> TelemetryPayload:
    """Valida uma mensagem sem persistir; a ingestão MQTT será adicionada depois."""
    try:
        return validate_telemetry(payload)
    except InvalidTelemetryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

if FRONTEND_DIR.is_dir():
    app.mount(
        "/dashboard",
        StaticFiles(directory=str(FRONTEND_DIR), html=True),
        name="dashboard",
    )


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """Abre o dashboard quando o backend e o frontend são executados juntos."""
    return RedirectResponse(url="/dashboard/")
