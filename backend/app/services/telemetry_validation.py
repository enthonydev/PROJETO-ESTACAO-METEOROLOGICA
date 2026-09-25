"""Validação da telemetria na fronteira do backend."""

from typing import Any

from pydantic import ValidationError

from app.schemas.telemetry import TelemetryPayload


class InvalidTelemetryError(ValueError):
    """Indica que o payload não atende ao contrato v1.0."""


def validate_telemetry(payload: dict[str, Any]) -> TelemetryPayload:
    """Converte e valida um payload recebido externamente."""
    try:
        return TelemetryPayload.model_validate(payload)
    except ValidationError as exc:
        raise InvalidTelemetryError("Payload de telemetria inválido") from exc
