"""Endpoints REST de consulta para o dashboard."""

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_station_service
from app.repositories.measurements import StationNotFoundError
from app.schemas.station import (
    MeasurementListResponse,
    MeasurementResponse,
    StationStatsResponse,
    StationSummary,
)
from app.services.station_queries import StationQueryService


router = APIRouter(prefix="/api/v1/stations", tags=["stations"])
RangeName = Literal["24h", "7d", "30d"]


def not_found(station_id: str) -> HTTPException:
    return HTTPException(
        status_code=404,
        detail=f"Estação não encontrada: {station_id}",
    )


@router.get("", response_model=list[StationSummary])
def list_stations(
    service: StationQueryService = Depends(get_station_service),
) -> list[StationSummary]:
    return service.stations()


@router.get("/{station_id}/latest", response_model=MeasurementResponse)
def latest_measurement(
    station_id: str,
    service: StationQueryService = Depends(get_station_service),
) -> MeasurementResponse:
    try:
        return service.latest(station_id)
    except StationNotFoundError as exc:
        raise not_found(station_id) from exc


@router.get("/{station_id}/measurements", response_model=MeasurementListResponse)
def measurements(
    station_id: str,
    range_name: RangeName = Query(default="24h", alias="range"),
    service: StationQueryService = Depends(get_station_service),
) -> MeasurementListResponse:
    try:
        return service.measurements(station_id, range_name)
    except StationNotFoundError as exc:
        raise not_found(station_id) from exc


@router.get("/{station_id}/summary", response_model=StationStatsResponse)
def summary(
    station_id: str,
    range_name: RangeName = Query(default="24h", alias="range"),
    service: StationQueryService = Depends(get_station_service),
) -> StationStatsResponse:
    try:
        return service.summary(station_id, range_name)
    except StationNotFoundError as exc:
        raise not_found(station_id) from exc
