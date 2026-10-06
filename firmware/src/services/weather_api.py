"""Abstração do estado meteorológico externo para a interface local."""

from models.state import WeatherState
from services.errors import WeatherProviderError


class WeatherStateService:
    def __init__(self, provider=None):
        self.provider = provider
        self.last_valid = WeatherState()
        self.last_error = None

    def update(self):
        if self.provider is None:
            return self.last_valid

        try:
            self.last_valid = self.provider.fetch()
            self.last_error = None
        except (OSError, TimeoutError, ValueError, WeatherProviderError) as exc:
            self.last_valid.stale = True
            self.last_error = exc

        return self.last_valid
