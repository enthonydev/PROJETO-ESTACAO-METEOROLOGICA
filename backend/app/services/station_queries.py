"""Serviço de consulta das estações e medições."""

from app.repositories.measurements import MeasurementRepository
from app.schemas.station import (
    MeasurementListResponse,
    MeasurementResponse,
    StationStatsResponse,
    StationSummary,
)
from app.services.measurement_rules import build_station_summary, ensure_supported_range


class StationQueryService:
    def __init__(self, repository: MeasurementRepository) -> None:
        self.repository = repository

    def stations(self) -> list[StationSummary]:
        return self.repository.list_stations()

    def latest(self, station_id: str) -> MeasurementResponse:
        return MeasurementResponse.model_validate(
            self.repository.latest(station_id).model_dump()
        )

    def measurements(self, station_id: str, range_name: str) -> MeasurementListResponse:
        supported_range = ensure_supported_range(range_name)
        items = [
            MeasurementResponse.model_validate(payload.model_dump())
            for payload in self.repository.history(station_id, supported_range)
        ]
        return MeasurementListResponse(
            station_id=station_id,
            range=supported_range,
            items=items,
        )

    def summary(self, station_id: str, range_name: str) -> StationStatsResponse:
        supported_range = ensure_supported_range(range_name)
        values = self.repository.history(station_id, supported_range)
        return build_station_summary(station_id, supported_range, values)
