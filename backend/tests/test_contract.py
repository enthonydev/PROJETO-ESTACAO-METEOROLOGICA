"""Cobertura complementar do contrato v1.0 na fronteira FastAPI."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.schemas.telemetry import TelemetryPayload
from app.services.telemetry_validation import InvalidTelemetryError, validate_telemetry


FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_valid_fixture_matches_contract_model() -> None:
    payload = validate_telemetry(load_fixture("telemetry-valid.json"))

    assert isinstance(payload, TelemetryPayload)
    assert payload.schema_version == "1.0"
    assert payload.timestamp.tzinfo is not None


def test_partial_fixture_preserves_absent_measurement() -> None:
    payload = validate_telemetry(load_fixture("telemetry-partial.json"))

    assert payload.measurements.temperature_c is None
    assert payload.quality.temperature == "error"


def test_invalid_fixture_is_rejected_by_contract_validation() -> None:
    with pytest.raises(InvalidTelemetryError):
        validate_telemetry(load_fixture("telemetry-invalid.json"))


def test_unknown_fields_are_rejected() -> None:
    payload = load_fixture("telemetry-valid.json")
    payload["unexpected"] = True

    with pytest.raises(ValidationError):
        TelemetryPayload.model_validate(payload)


def test_unsupported_schema_version_is_rejected() -> None:
    payload = load_fixture("telemetry-valid.json")
    payload["schema_version"] = "2.0"

    with pytest.raises(ValidationError):
        TelemetryPayload.model_validate(payload)


def test_empty_station_id_is_rejected() -> None:
    payload = load_fixture("telemetry-valid.json")
    payload["station_id"] = ""

    with pytest.raises(ValidationError):
        TelemetryPayload.model_validate(payload)
