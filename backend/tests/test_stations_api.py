"""Testes dos endpoints REST usados pelo dashboard."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_stations_returns_demo_station() -> None:
    response = client.get("/api/v1/stations")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 1
    assert payload[0]["station_id"] == "estacao-01"


def test_latest_returns_contract_compatible_payload() -> None:
    response = client.get("/api/v1/stations/estacao-01/latest")

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema_version"] == "1.0"
    assert payload["station_id"] == "estacao-01"
    assert "measurements" in payload
    assert payload["measurements"]["rain_mm"] is None
    assert payload["quality"]["rain"] == "error"


def test_measurements_supports_dashboard_ranges() -> None:
    response = client.get("/api/v1/stations/estacao-01/measurements?range=24h")

    assert response.status_code == 200
    payload = response.json()
    assert payload["station_id"] == "estacao-01"
    assert payload["range"] == "24h"
    assert len(payload["items"]) >= 2


def test_summary_returns_stats() -> None:
    response = client.get("/api/v1/stations/estacao-01/summary?range=24h")

    assert response.status_code == 200
    payload = response.json()
    assert payload["temperature_c"]["min"] is not None
    assert payload["temperature_c"]["avg"] is not None
    assert payload["temperature_c"]["max"] is not None
    assert payload["station_id"] == "estacao-01"


def test_unknown_station_returns_404() -> None:
    response = client.get("/api/v1/stations/inexistente/latest")

    assert response.status_code == 404


def test_invalid_range_is_rejected() -> None:
    response = client.get("/api/v1/stations/estacao-01/measurements?range=1h")

    assert response.status_code == 422


def test_root_redirects_to_dashboard() -> None:
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (307, 308)
    assert response.headers["location"] == "/dashboard/"


def test_dashboard_is_served_by_backend() -> None:
    response = client.get("/dashboard/")

    assert response.status_code == 200
    assert "Painel ambiental" in response.text
