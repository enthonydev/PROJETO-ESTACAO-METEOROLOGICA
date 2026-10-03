"""Dependências compartilhadas da API."""

from functools import lru_cache

from app.core.config import settings
from app.core.demo_data import build_demo_payloads
from app.repositories.measurements import (
    InMemoryMeasurementRepository,
    MeasurementRepository,
)
from app.repositories.postgres_measurements import PostgresMeasurementRepository
from app.services.station_queries import StationQueryService


@lru_cache(maxsize=1)
def get_measurement_repository() -> MeasurementRepository:
    """Seleciona PostgreSQL quando configurado; caso contrário usa memória."""
    if settings.database_url:
        return PostgresMeasurementRepository(settings.database_url)

    return InMemoryMeasurementRepository(build_demo_payloads())


def get_station_service() -> StationQueryService:
    return StationQueryService(get_measurement_repository())
