"""Testes mínimos do skeleton FastAPI e do contrato de entrada."""

import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


FIXTURES = Path(__file__).parent / "fixtures"
client = TestClient(app)


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_valid_payload_is_returned_normalized() -> None:
    response = client.post(
        "/api/v1/telemetry/validate", json=load_fixture("telemetry-valid.json")
    )

    assert response.status_code == 200
    assert response.json()["schema_version"] == "1.0"
    assert response.json()["station_id"] == "estacao-01"


def test_partial_payload_preserves_null_and_quality_error() -> None:
    response = client.post(
        "/api/v1/telemetry/validate", json=load_fixture("telemetry-partial.json")
    )

    assert response.status_code == 200
    assert response.json()["measurements"]["temperature_c"] is None
    assert response.json()["quality"]["temperature"] == "error"


def test_invalid_payload_is_rejected() -> None:
    response = client.post(
        "/api/v1/telemetry/validate", json=load_fixture("telemetry-invalid.json")
    )

    assert response.status_code == 422
