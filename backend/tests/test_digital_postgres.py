"""Ensaio PostgreSQL para estados digitais; exige TEST_DATABASE_URL."""
import os
from pathlib import Path

import psycopg
import pytest

from app.repositories.digital_states import PostgresDigitalStates
from app.schemas.digital import DigitalState

URL = os.getenv("TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not URL, reason="TEST_DATABASE_URL nao configurada")


def test_digital_postgres_roundtrip():
    root = Path(__file__).resolve().parents[2]
    migration1 = (root / "database/migrations/001_schema_inicial.sql").read_text(encoding="utf-8")
    migration2 = (root / "database/migrations/002_estado_digital.sql").read_text(encoding="utf-8")
    with psycopg.connect(URL, autocommit=True) as conn, conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS station_digital_states CASCADE")
        cur.execute("DROP TABLE IF EXISTS measurement_quality CASCADE")
        cur.execute("DROP TABLE IF EXISTS measurements CASCADE")
        cur.execute("DROP TABLE IF EXISTS stations CASCADE")
        cur.execute(migration1)
        cur.execute(migration2)

    repo = PostgresDigitalStates(URL)
    state = DigitalState(
        station_id="estacao-fisica",
        timestamp="2026-11-04T20:00:00Z",
        rain_detected=True,
        dark=False,
    )
    repo.add(state)
    result = repo.latest("estacao-fisica")
    assert result.rain_detected is True
    assert result.dark is False
    assert result.station_id == "estacao-fisica"
