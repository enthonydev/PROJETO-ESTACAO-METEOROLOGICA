"""Implementação PostgreSQL do repositório de medições."""

from __future__ import annotations

from psycopg import connect
from psycopg.rows import dict_row

from app.repositories.measurements import (
    MeasurementNotFoundError,
    StationNotFoundError,
)
from app.schemas.station import StationSummary
from app.schemas.telemetry import Location, Measurements, Quality, TelemetryPayload
from app.services.measurement_rules import RANGE_INTERVAL, ensure_supported_range



class PostgresMeasurementRepository:
    """Persistência compatível com database/migrations/001_schema_inicial.sql."""

    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    def _connection(self):
        return connect(self.database_url, row_factory=dict_row)

    @staticmethod
    def _payload_from_rows(measurement: dict, quality_rows: list[dict]) -> TelemetryPayload:
        quality_by_metric = {row["metric"]: row["status"] for row in quality_rows}

        return TelemetryPayload(
            schema_version="1.0",
            station_id=measurement["station_code"],
            timestamp=measurement["measured_at"],
            location=Location(
                latitude=measurement["latitude"],
                longitude=measurement["longitude"],
            ),
            measurements=Measurements(
                temperature_c=measurement["temperature_c"],
                humidity_pct=measurement["humidity_pct"],
                pressure_hpa=measurement["pressure_hpa"],
                air_quality_raw=measurement["air_quality_raw"],
                luminosity_pct=measurement["luminosity_pct"],
                rain_mm=measurement["rain_mm"],
            ),
            quality=Quality(
                temperature=quality_by_metric.get("temperature", "error"),
                humidity=quality_by_metric.get("humidity", "error"),
                pressure=quality_by_metric.get("pressure", "error"),
                air_quality=quality_by_metric.get("air_quality", "error"),
                luminosity=quality_by_metric.get("luminosity", "error"),
                rain=quality_by_metric.get("rain", "error"),
            ),
        )

    def list_stations(self) -> list[StationSummary]:
        query = """
            SELECT
                s.code AS station_id,
                s.name,
                s.active,
                s.latitude,
                s.longitude,
                MAX(m.measured_at) AS last_measurement_at
            FROM stations s
            LEFT JOIN measurements m ON m.station_id = s.id
            GROUP BY s.id
            ORDER BY s.code
        """

        with self._connection() as conn, conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

        return [
            StationSummary(
                station_id=row["station_id"],
                name=row["name"],
                active=row["active"],
                location=Location(
                    latitude=row["latitude"],
                    longitude=row["longitude"],
                ),
                last_measurement_at=row["last_measurement_at"],
            )
            for row in rows
        ]

    def _measurement_rows(self, station_id: str, range_name: str | None = None) -> list[dict]:
        params: list[object] = [station_id]
        range_clause = ""

        if range_name is not None:
            supported_range = ensure_supported_range(range_name)
            range_clause = "AND m.measured_at >= NOW() - %s::interval"
            params.append(RANGE_INTERVAL[supported_range])

        query = f"""
            SELECT
                m.id,
                s.code AS station_code,
                s.latitude,
                s.longitude,
                m.measured_at,
                m.temperature_c,
                m.humidity_pct,
                m.pressure_hpa,
                m.air_quality_raw,
                m.luminosity_pct,
                m.rain_mm
            FROM measurements m
            JOIN stations s ON s.id = m.station_id
            WHERE s.code = %s
            {range_clause}
            ORDER BY m.measured_at ASC
        """

        with self._connection() as conn, conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

        if not rows:
            with self._connection() as conn, conn.cursor() as cur:
                cur.execute("SELECT 1 FROM stations WHERE code = %s", (station_id,))
                if cur.fetchone() is None:
                    raise StationNotFoundError(station_id)
            raise MeasurementNotFoundError(station_id)

        return rows

    def _quality_for_ids(self, ids: list[int]) -> dict[int, list[dict]]:
        if not ids:
            return {}

        query = """
            SELECT measurement_id, metric, status
            FROM measurement_quality
            WHERE measurement_id = ANY(%s)
            ORDER BY measurement_id, metric
        """

        with self._connection() as conn, conn.cursor() as cur:
            cur.execute(query, (ids,))
            rows = cur.fetchall()

        result: dict[int, list[dict]] = {measurement_id: [] for measurement_id in ids}
        for row in rows:
            result[row["measurement_id"]].append(row)
        return result

    def latest(self, station_id: str) -> TelemetryPayload:
        rows = self._measurement_rows(station_id)
        row = rows[-1]
        quality = self._quality_for_ids([row["id"]])
        return self._payload_from_rows(row, quality.get(row["id"], []))

    def history(self, station_id: str, range_name: str) -> list[TelemetryPayload]:
        rows = self._measurement_rows(station_id, range_name)
        quality = self._quality_for_ids([row["id"] for row in rows])

        return [
            self._payload_from_rows(row, quality.get(row["id"], []))
            for row in rows
        ]

    def add(self, payload: TelemetryPayload) -> None:
        station_name = payload.station_id.replace("-", " ").title()

        with self._connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO stations (code, name, latitude, longitude)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (code) DO UPDATE
                SET
                    latitude = COALESCE(EXCLUDED.latitude, stations.latitude),
                    longitude = COALESCE(EXCLUDED.longitude, stations.longitude),
                    updated_at = NOW()
                RETURNING id
                """,
                (
                    payload.station_id,
                    station_name,
                    payload.location.latitude,
                    payload.location.longitude,
                ),
            )
            station_db_id = cur.fetchone()["id"]

            values = payload.measurements
            cur.execute(
                """
                INSERT INTO measurements (
                    station_id,
                    measured_at,
                    temperature_c,
                    humidity_pct,
                    pressure_hpa,
                    air_quality_raw,
                    luminosity_pct,
                    rain_mm
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    station_db_id,
                    payload.timestamp,
                    values.temperature_c,
                    values.humidity_pct,
                    values.pressure_hpa,
                    values.air_quality_raw,
                    values.luminosity_pct,
                    values.rain_mm,
                ),
            )
            measurement_id = cur.fetchone()["id"]

            quality = payload.quality.model_dump()
            cur.executemany(
                """
                INSERT INTO measurement_quality (measurement_id, metric, status)
                VALUES (%s, %s, %s)
                """,
                [
                    (measurement_id, metric, status)
                    for metric, status in quality.items()
                ],
            )
