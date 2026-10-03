"""Integração ponta a ponta com broker MQTT e PostgreSQL reais em CI."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time
from uuid import uuid4

import httpx
import paho.mqtt.publish as publish
import psycopg
import pytest


DATABASE_URL = os.getenv("TEST_DATABASE_URL")
MQTT_HOST = os.getenv("TEST_MQTT_BROKER_HOST")
MQTT_PORT = int(os.getenv("TEST_MQTT_BROKER_PORT", "1883"))

pytestmark = pytest.mark.skipif(
    not DATABASE_URL or not MQTT_HOST,
    reason="TEST_DATABASE_URL e TEST_MQTT_BROKER_HOST são obrigatórios",
)

ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
API_PORT = 8010
API_BASE = f"http://127.0.0.1:{API_PORT}"


def reset_database() -> None:
    migration = (
        ROOT / "database" / "migrations" / "001_schema_inicial.sql"
    ).read_text(encoding="utf-8")

    with psycopg.connect(DATABASE_URL, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS measurement_quality CASCADE")
            cur.execute("DROP TABLE IF EXISTS measurements CASCADE")
            cur.execute("DROP TABLE IF EXISTS stations CASCADE")
            cur.execute(migration)


def process_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(BACKEND)
    env["DATABASE_URL"] = DATABASE_URL
    env["MQTT_BROKER_HOST"] = MQTT_HOST
    env["MQTT_BROKER_PORT"] = str(MQTT_PORT)
    env["MQTT_SUBSCRIPTION_TOPIC"] = "estacao/+/telemetry"
    env["ENABLE_HTTP_INGESTION"] = "false"
    env["PYTHONUNBUFFERED"] = "1"
    return env


def wait_for_api(timeout_seconds: float = 15.0) -> None:
    deadline = time.monotonic() + timeout_seconds

    while time.monotonic() < deadline:
        try:
            response = httpx.get(f"{API_BASE}/health", timeout=1.0)
            if response.status_code == 200:
                return
        except httpx.HTTPError:
            pass
        time.sleep(0.25)

    raise AssertionError("FastAPI não ficou disponível dentro do prazo")


def wait_for_station(station_id: str, timeout_seconds: float = 15.0) -> dict:
    deadline = time.monotonic() + timeout_seconds
    last_status = None

    while time.monotonic() < deadline:
        try:
            response = httpx.get(
                f"{API_BASE}/api/v1/stations/{station_id}/latest",
                timeout=1.5,
            )
            last_status = response.status_code
            if response.status_code == 200:
                return response.json()
        except httpx.HTTPError:
            pass
        time.sleep(0.35)

    raise AssertionError(
        f"Telemetria MQTT não chegou à API dentro do prazo; último status={last_status}"
    )


def stop_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return

    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def test_broker_mqtt_to_postgres_to_rest() -> None:
    reset_database()

    env = process_env()
    api = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(API_PORT),
        ],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    worker = subprocess.Popen(
        [sys.executable, "-m", "app.workers.mqtt_consumer"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    station_id = f"estacao-ci-{uuid4().hex[:8]}"
    topic = f"estacao/{station_id}/telemetry"
    payload = {
        "schema_version": "1.0",
        "station_id": station_id,
        "timestamp": "2026-10-02T22:45:00Z",
        "location": {"latitude": None, "longitude": None},
        "measurements": {
            "temperature_c": 26.3,
            "humidity_pct": 58,
            "pressure_hpa": 1010,
            "air_quality_raw": 179,
            "luminosity_pct": 51,
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

    try:
        wait_for_api()

        # Mensagem retida evita corrida entre publish e subscribe do worker no CI.
        publish.single(
            topic,
            payload=json.dumps(payload),
            qos=1,
            retain=True,
            hostname=MQTT_HOST,
            port=MQTT_PORT,
        )

        latest = wait_for_station(station_id)

        assert latest["station_id"] == station_id
        assert latest["schema_version"] == "1.0"
        assert latest["measurements"]["temperature_c"] == 26.3
        assert latest["quality"]["air_quality"] == "suspect"

        history = httpx.get(
            f"{API_BASE}/api/v1/stations/{station_id}/measurements",
            params={"range": "24h"},
            timeout=2.0,
        )
        assert history.status_code == 200
        assert len(history.json()["items"]) >= 1

        dashboard = httpx.get(f"{API_BASE}/dashboard/", timeout=2.0)
        assert dashboard.status_code == 200
        assert "Painel ambiental" in dashboard.text
    finally:
        try:
            publish.single(
                topic,
                payload=None,
                qos=1,
                retain=True,
                hostname=MQTT_HOST,
                port=MQTT_PORT,
            )
        except Exception:
            pass
        stop_process(worker)
        stop_process(api)
