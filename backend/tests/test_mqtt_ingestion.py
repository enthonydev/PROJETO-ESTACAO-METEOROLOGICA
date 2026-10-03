"""Testes do processamento MQTT sem broker físico."""

import json

import pytest

from app.repositories.measurements import InMemoryMeasurementRepository
from app.services.mqtt_ingestion import InvalidMqttMessageError, process_mqtt_message


def payload(station_id: str = "estacao-01") -> dict:
    return {
        "schema_version": "1.0",
        "station_id": station_id,
        "timestamp": "2026-10-02T22:00:00Z",
        "location": {"latitude": None, "longitude": None},
        "measurements": {
            "temperature_c": 25.1,
            "humidity_pct": 61,
            "pressure_hpa": 1011,
            "air_quality_raw": 180,
            "luminosity_pct": 40,
            "rain_mm": None,
        },
        "quality": {
            "temperature": "ok",
            "humidity": "ok",
            "pressure": "ok",
            "air_quality": "suspect",
            "luminosity": "ok",
            "rain": "error",
        },
    }


def test_mqtt_message_is_persisted() -> None:
    repository = InMemoryMeasurementRepository()

    result = process_mqtt_message(
        "estacao/estacao-01/telemetry",
        json.dumps(payload()).encode(),
        repository,
    )

    assert result.station_id == "estacao-01"
    assert repository.latest("estacao-01").measurements.temperature_c == 25.1


def test_topic_station_must_match_payload() -> None:
    repository = InMemoryMeasurementRepository()

    with pytest.raises(InvalidMqttMessageError):
        process_mqtt_message(
            "estacao/outra/telemetry",
            json.dumps(payload()).encode(),
            repository,
        )


def test_invalid_topic_is_rejected() -> None:
    repository = InMemoryMeasurementRepository()

    with pytest.raises(InvalidMqttMessageError):
        process_mqtt_message(
            "qualquer/topico",
            json.dumps(payload()).encode(),
            repository,
        )


def test_invalid_json_is_rejected() -> None:
    repository = InMemoryMeasurementRepository()

    with pytest.raises(InvalidMqttMessageError):
        process_mqtt_message(
            "estacao/estacao-01/telemetry",
            b"{invalido",
            repository,
        )
