"""Schemas das consultas REST do dashboard."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.schemas.telemetry import Location, Measurements, Quality


class StrictResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")


class StationSummary(StrictResponse):
    station_id: str
    name: str
    active: bool
    location: Location
    last_measurement_at: datetime | None = None


class MeasurementResponse(StrictResponse):
    schema_version: Literal["1.0"] = "1.0"
    station_id: str
    timestamp: datetime
    location: Location
    measurements: Measurements
    quality: Quality


class MeasurementListResponse(StrictResponse):
    station_id: str
    range: Literal["24h", "7d", "30d"]
    items: list[MeasurementResponse]


class MetricStats(StrictResponse):
    min: float | None = None
    avg: float | None = None
    max: float | None = None


class StationStatsResponse(StrictResponse):
    station_id: str
    range: Literal["24h", "7d", "30d"]
    temperature_c: MetricStats
    humidity_pct: MetricStats
    pressure_hpa: MetricStats
    air_quality_raw: MetricStats
    luminosity_pct: MetricStats
