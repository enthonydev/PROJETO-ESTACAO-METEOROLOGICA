"""Repositório de medições para consultas do dashboard."""

from __future__ import annotations

from datetime import timedelta
from typing import Iterable, Protocol

from app.schemas.station import StationSummary
from app.schemas.telemetry import TelemetryPayload
from app.services.measurement_rules import RANGE_DELTA, ensure_supported_range


class StationNotFoundError(LookupError):
    """Indica que a estação solicitada não existe."""


class MeasurementNotFoundError(LookupError):
    """Indica que a estação ainda não possui medições."""


class MeasurementRepository(Protocol):
    def list_stations(self) -> list[StationSummary]: ...
    def latest(self, station_id: str) -> TelemetryPayload: ...
    def history(self, station_id: str, range_name: str) -> list[TelemetryPayload]: ...
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
            result.append(StationSummary(
                station_id=station_id,
                name=station_id.replace("-", " ").title(),
                active=True,
                location=latest.location,
                last_measurement_at=latest.timestamp,
            ))
        return result

    def latest(self, station_id: str) -> TelemetryPayload:
        return max(self._station_payloads(station_id), key=lambda item: item.timestamp)

    def history(self, station_id: str, range_name: str) -> list[TelemetryPayload]:
        supported_range = ensure_supported_range(range_name)
        values = self._station_payloads(station_id)
        latest_timestamp = max(item.timestamp for item in values)
        cutoff = latest_timestamp - RANGE_DELTA[supported_range]
        return [item for item in values if item.timestamp >= cutoff]

    def add(self, payload: TelemetryPayload) -> None:
        self._payloads.append(payload)
        self._payloads.sort(key=lambda item: item.timestamp)
