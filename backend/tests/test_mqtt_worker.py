"""Testes de segurança operacional do worker MQTT."""

from types import SimpleNamespace

import pytest

import app.workers.mqtt_consumer as mqtt_consumer


def test_worker_requires_shared_database(monkeypatch) -> None:
    monkeypatch.setattr(
        mqtt_consumer,
        "settings",
        SimpleNamespace(
            database_url=None,
            log_level="INFO",
            mqtt_broker_host="localhost",
            mqtt_broker_port=1883,
            mqtt_subscription_topic="estacao/+/telemetry",
        ),
    )

    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        mqtt_consumer.main()
