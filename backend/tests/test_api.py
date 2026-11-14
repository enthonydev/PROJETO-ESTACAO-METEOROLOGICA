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


def test_ct03_professor_rejects_temperature_150_c():
    payload = load_fixture("telemetry-valid.json")
    payload["measurements"]["temperature_c"] = 150.0
    response = client.post("/api/v1/telemetry/validate", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"] == "Payload de telemetria inválido"


def test_dht22_temperature_boundaries_are_inclusive():
    for temperature, expected in [(-40.0, 200), (80.0, 200), (-40.1, 422), (80.1, 422)]:
        payload = load_fixture("telemetry-valid.json")
        payload["measurements"]["temperature_c"] = temperature
        assert client.post("/api/v1/telemetry/validate", json=payload).status_code == expected
