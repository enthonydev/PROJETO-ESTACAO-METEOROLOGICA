"""Abstração do estado meteorológico externo para a interface local."""

from models.state import WeatherState


class WeatherStateService:
    def __init__(self, provider=None):
        self.provider = provider
        self.last_valid = WeatherState()

    def update(self):
        if self.provider is None:
            return self.last_valid
        try:
            self.last_valid = self.provider.fetch()
        except Exception:
            self.last_valid.stale = True
        return self.last_valid
