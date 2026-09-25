"""Aquisição de sensores por meio de drivers injetados."""

from models.state import SensorSnapshot


class SensorService:
    def __init__(self, drivers=None):
        self.drivers = drivers or {}

    def read(self):
        measurements = {}
        quality = {}
        for name, driver in self.drivers.items():
            try:
                value = driver.read()
                measurements[name] = value
                quality[name] = "ok"
            except Exception:
                measurements[name] = None
                quality[name] = "error"
        return SensorSnapshot(measurements, quality)
