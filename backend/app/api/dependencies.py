"""Dependências compartilhadas da API."""

from functools import lru_cache

from app.core.demo_data import build_demo_payloads
from app.repositories.measurements import InMemoryMeasurementRepository
from app.services.station_queries import StationQueryService


@lru_cache(maxsize=1)
def get_station_service() -> StationQueryService:
    """Retorna o serviço padrão para desenvolvimento sem hardware."""
    repository = InMemoryMeasurementRepository(build_demo_payloads())
    return StationQueryService(repository)
