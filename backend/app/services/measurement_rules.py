"""Regras de domínio compartilhadas para consultas de medições."""

from datetime import timedelta
from statistics import fmean
from typing import Literal

from app.schemas.station import MetricStats, StationStatsResponse
from app.schemas.telemetry import TelemetryPayload

RangeName = Literal["24h", "7d", "30d"]

RANGE_DELTA: dict[RangeName, timedelta] = {
    "24h": timedelta(hours=24),
    "7d": timedelta(days=7),
    "30d": timedelta(days=30),
}

RANGE_INTERVAL: dict[RangeName, str] = {
    "24h": "24 hours",
    "7d": "7 days",
    "30d": "30 days",
}

METRICS = (
    "temperature_c",
    "humidity_pct",
    "pressure_hpa",
    "air_quality_raw",
    "luminosity_pct",
)


def ensure_supported_range(range_name: str) -> RangeName:
    if range_name not in RANGE_DELTA:
        raise ValueError(f"Período não suportado: {range_name}")
    return range_name


def build_station_summary(
    station_id: str,
    range_name: str,
    values: list[TelemetryPayload],
) -> StationStatsResponse:
    """Calcula estatísticas sem acoplar a regra ao mecanismo de persistência."""
    ensure_supported_range(range_name)

    def stats(metric: str) -> MetricStats:
        numbers = [
            getattr(item.measurements, metric)
            for item in values
            if getattr(item.measurements, metric) is not None
        ]
        if not numbers:
            return MetricStats()
        return MetricStats(min=min(numbers), avg=fmean(numbers), max=max(numbers))

    return StationStatsResponse(
        station_id=station_id,
        range=range_name,
        temperature_c=stats("temperature_c"),
        humidity_pct=stats("humidity_pct"),
        pressure_hpa=stats("pressure_hpa"),
        air_quality_raw=stats("air_quality_raw"),
        luminosity_pct=stats("luminosity_pct"),
    )
