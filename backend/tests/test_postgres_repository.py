"""Teste de integração do repositório PostgreSQL em runtime."""

import os
from pathlib import Path

import psycopg
import pytest

from app.repositories.postgres_measurements import PostgresMeasurementRepository
from app.schemas.telemetry import Location, Measurements, Quality, TelemetryPayload
from app.services.station_queries import StationQueryService


DATABASE_URL = os.getenv("TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(
    not DATABASE_URL,
    reason="TEST_DATABASE_URL não configurada",
)


def reset_database() -> None:
    migration = (
        Path(__file__).resolve().parents[2]
        / "database"
        / "migrations"
        / "001_schema_inicial.sql"
    ).read_text(encoding="utf-8")

    with psycopg.connect(DATABASE_URL, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS measurement_quality CASCADE")
            cur.execute("DROP TABLE IF EXISTS measurements CASCADE")
            cur.execute("DROP TABLE IF EXISTS stations CASCADE")
            cur.execute(migration)


def test_postgres_roundtrip() -> None:
    reset_database()
    repository = PostgresMeasurementRepository(DATABASE_URL)

    payload = TelemetryPayload(
        schema_version="1.0",
        station_id="estacao-pg",
        timestamp="2026-10-02T22:00:00Z",
        location=Location(latitude=-23.0, longitude=-46.0),
        measurements=Measurements(
            temperature_c=24.2,
            humidity_pct=62,
            pressure_hpa=1012,
            air_quality_raw=181,
            luminosity_pct=48,
            rain_mm=None,
        ),
        quality=Quality(
            temperature="ok",
            humidity="ok",
            pressure="ok",
            air_quality="suspect",
            luminosity="ok",
            rain="error",
        ),
    )

    repository.add(payload)

    latest = repository.latest("estacao-pg")
    history = repository.history("estacao-pg", "24h")
    summary = StationQueryService(repository).summary("estacao-pg", "24h")

    assert latest.station_id == "estacao-pg"
    assert latest.measurements.temperature_c == 24.2
    assert latest.quality.air_quality == "suspect"
    assert len(history) == 1
    assert summary.temperature_c.avg == 24.2
