"""Composição inicial do firmware; pinagem e drivers concretos permanecem TBD."""

from services.connectivity import Connectivity
from services.sensor_service import SensorService
from services.time_service import TimeService
from services.weather_api import WeatherStateService


class FirmwareApplication:
    """Agrupa serviços por injeção de dependências para futura integração física."""

    def __init__(
        self,
        sensor_drivers=None,
        weather_provider=None,
        primary_time_source=None,
        fallback_time_source=None,
    ):
        self.sensor_service = SensorService(sensor_drivers)
        self.weather_service = WeatherStateService(weather_provider)
        self.time_service = TimeService(primary_time_source, fallback_time_source)
        self.connectivity = Connectivity()

    def read_local_state(self):
        return self.sensor_service.read()
