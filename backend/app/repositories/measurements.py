"""Repositório de medições para consultas do dashboard."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from statistics import fmean
from typing import Iterable, Protocol

from app.schemas.station import MetricStats, StationStatsResponse, StationSummary
from app.schemas.telemetry import Location, TelemetryPayload


RANGE_DELTA = {
    "24h": timedelta(hours=24),
    "7d": timedelta(days=7),
    "30d": timedelta(days=30),
}

METRICS = (
    "temperature_c",
    "humidity_pct",
    "pressure_hpa",
    "air_quality_raw",
    "luminosity_pct",
)


class StationNotFoundError(LookupError):
    """Indica que a estação solicitada não existe."""


class MeasurementNotFoundError(LookupError):
    """Indica que a estação ainda não possui medições."""


class MeasurementRepository(Protocol):
    def list_stations(self) -> list[StationSummary]: ...
    def latest(self, station_id: str) -> TelemetryPayload: ...
    def history(self, station_id: str, range_name: str) -> list[TelemetryPayload]: ...
    def summary(self, station_id: str, range_name: str) -> StationStatsResponse: ...
    def add(self, payload: TelemetryPayload) -> None: ...


class InMemoryMeasurementRepository:
    """Implementação para desenvolvimento, testes e integração sem hardware."""

    def __init__(self, payloads: Iterable[TelemetryPayload] = ()) -> None:
        self._payloads: list[TelemetryPayload] = sorted(
            list(payloads), key=lambda item: item.timestamp
        )

    def _station_payloads(self, station_id: str) -> list[TelemetryPayload]:
        values = [item for item in self._payloads if item.station_id == station_id]
        if not values:
            raise StationNotFoundError(station_id)
        return values

    def list_stations(self) -> list[StationSummary]:
        station_ids = sorted({item.station_id for item in self._payloads})
        result: list[StationSummary] = []

        for station_id in station_ids:
            latest = self.latest(station_id)
            result.append(
                StationSummary(
                    station_id=station_id,
                    name=station_id.replace("-", " ").title(),
                    active=True,
                    location=latest.location,
                    last_measurement_at=latest.timestamp,
                )
            )

        return result

    def latest(self, station_id: str) -> TelemetryPayload:
        values = self._station_payloads(station_id)
        return max(values, key=lambda item: item.timestamp)

    def history(self, station_id: str, range_name: str) -> list[TelemetryPayload]:
        if range_name not in RANGE_DELTA:
            raise ValueError(f"Período não suportado: {range_name}")

        values = self._station_payloads(station_id)
        latest_timestamp = max(item.timestamp for item in values)
        cutoff = latest_timestamp - RANGE_DELTA[range_name]

        return [item for item in values if item.timestamp >= cutoff]

    def summary(self, station_id: str, range_name: str) -> StationStatsResponse:
        values = self.history(station_id, range_name)

        def stats(metric: str) -> MetricStats:
            numbers = [
                getattr(item.measurements, metric)
                for item in values
                if getattr(item.measurements, metric) is not None
            ]
            if not numbers:
                return MetricStats()
            return MetricStats(
                min=min(numbers),
                avg=fmean(numbers),
                max=max(numbers),
            )

        return StationStatsResponse(
            station_id=station_id,
            range=range_name,
            temperature_c=stats("temperature_c"),
            humidity_pct=stats("humidity_pct"),
            pressure_hpa=stats("pressure_hpa"),
            air_quality_raw=stats("air_quality_raw"),
            luminosity_pct=stats("luminosity_pct"),
        )

    def add(self, payload: TelemetryPayload) -> None:
        self._payloads.append(payload)
        self._payloads.sort(key=lambda item: item.timestamp)
