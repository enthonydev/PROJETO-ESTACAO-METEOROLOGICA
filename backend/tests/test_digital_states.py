"""Testes do canal digital auxiliar, sem simular sua origem como física."""
from datetime import datetime, timezone
import json
from types import SimpleNamespace

from fastapi.testclient import TestClient
import pytest

from app.api.digital import get_digital_states_repository
from app.main import app
from app.repositories.digital_states import InMemoryDigitalStates
from app.schemas.digital import DigitalState
import app.api.digital as digital_api
import app.workers.mqtt_consumer as mqtt_consumer


@pytest.fixture
def local_repo(monkeypatch):
    repo = InMemoryDigitalStates()
    app.dependency_overrides[get_digital_states_repository] = lambda: repo
    monkeypatch.setattr(digital_api, "settings", SimpleNamespace(enable_http_ingestion=True))
    yield repo
    app.dependency_overrides.clear()


def payload(rain=False, dark=False):
    return {
        "station_id": "estacao-esp32-real",
        "timestamp": "2026-11-04T19:30:00Z",
        "rain_detected": rain,
        "dark": dark,
    }


def test_http_roundtrip_digital(local_repo):
    client = TestClient(app)
    response = client.post("/api/v1/digital", json=payload(True, False))
    assert response.status_code == 201
    result = client.get("/api/v1/stations/estacao-esp32-real/digital/latest")
    assert result.status_code == 200
    assert result.json()["rain_detected"] is True
    assert result.json()["dark"] is False


def test_invalid_bool_rejected(local_repo):
    p = payload()
    p["rain_detected"] = "sim"
    assert TestClient(app).post("/api/v1/digital", json=p).status_code == 422


def test_newer_state_wins_in_memory():
    repo = InMemoryDigitalStates()
    first = DigitalState.model_validate(payload(True, False))
    second = DigitalState.model_validate({**payload(False, True), "timestamp": "2026-11-04T19:25:00Z"})
    repo.add(first)
    repo.add(second)
    assert repo.latest("estacao-esp32-real").rain_detected is True


def test_worker_consumes_separate_mqtt_topic(monkeypatch):
    repository = InMemoryDigitalStates()
    monkeypatch.setattr(mqtt_consumer, "get_digital_states_repository", lambda: repository)
    message = SimpleNamespace(topic="estacao/estacao-esp32-real/digital", payload=json.dumps(payload(False, True)).encode())
    mqtt_consumer.on_message(None, None, message)
    assert repository.latest("estacao-esp32-real").dark is True


def test_worker_rejects_mismatched_topic(monkeypatch):
    repository = InMemoryDigitalStates()
    monkeypatch.setattr(mqtt_consumer, "get_digital_states_repository", lambda: repository)
    message = SimpleNamespace(topic="estacao/outra/digital", payload=json.dumps(payload()).encode())
    mqtt_consumer.on_message(None, None, message)
    with pytest.raises(LookupError):
        repository.latest("estacao-esp32-real")


def test_worker_subscribes_both_topics():
    seen = []
    client = SimpleNamespace(subscribe=lambda topic: seen.append(topic))
    mqtt_consumer.on_connect(client, None, None, 0)
    assert "estacao/+/telemetry" in seen
    assert "estacao/+/digital" in seen
