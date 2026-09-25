"""Modelos de estado usados entre serviços, tarefas e renderizadores."""


class SensorSnapshot:
    def __init__(self, measurements=None, quality=None):
        self.measurements = measurements or {}
        self.quality = quality or {}


class WeatherState:
    def __init__(self, external=None, local=None, stale=False):
        self.external = external or {}
        self.local = local or {}
        self.stale = stale


class ClockState:
    def __init__(self, year, month, day, weekday, hour, minute):
        self.year = year
        self.month = month
        self.day = day
        self.weekday = weekday
        self.hour = hour
        self.minute = minute
