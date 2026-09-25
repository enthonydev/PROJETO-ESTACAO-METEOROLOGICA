"""Resolução de tempo por fonte injetada, sem assumir hardware ou rede."""

from models.state import ClockState


class TimeService:
    def __init__(self, primary_source=None, fallback_source=None):
        self.primary_source = primary_source
        self.fallback_source = fallback_source

    def current(self):
        source = self.primary_source or self.fallback_source
        if source is None:
            return None
        return source.read()

    @staticmethod
    def to_clock_state(value):
        if value is None:
            return None
        return ClockState(
            year=value[0],
            month=value[1],
            day=value[2],
            weekday=value[6],
            hour=value[3],
            minute=value[4],
        )
