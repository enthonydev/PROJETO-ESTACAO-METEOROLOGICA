"""Serviço de consulta das estações e medições."""

from app.repositories.measurements import MeasurementRepository
from app.schemas.station import (
    MeasurementListResponse,
    MeasurementResponse,
    StationStatsResponse,
    StationSummary,
)


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
        items = [
            MeasurementResponse.model_validate(payload.model_dump())
            for payload in self.repository.history(station_id, range_name)
        ]
        return MeasurementListResponse(
            station_id=station_id,
            range=range_name,
            items=items,
        )

    def summary(self, station_id: str, range_name: str) -> StationStatsResponse:
        return self.repository.summary(station_id, range_name)
