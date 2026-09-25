"""Modelos de entrada para o contrato de telemetria v1.0."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


QualityStatus = Literal["ok", "suspect", "invalid", "error"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Location(StrictModel):
    latitude: float | None = None
    longitude: float | None = None


class Measurements(StrictModel):
    temperature_c: float | None = None
    humidity_pct: float | None = None
    pressure_hpa: float | None = None
    air_quality_raw: float | None = None
    luminosity_pct: float | None = None
    rain_mm: float | None = None


class Quality(StrictModel):
    temperature: QualityStatus
    humidity: QualityStatus
    pressure: QualityStatus
    air_quality: QualityStatus
    luminosity: QualityStatus
    rain: QualityStatus


class TelemetryPayload(StrictModel):
    schema_version: Literal["1.0"]
    station_id: str = Field(min_length=1)
    timestamp: datetime
    location: Location
    measurements: Measurements
    quality: Quality


class HealthResponse(StrictModel):
    status: Literal["ok"]
    service: str
