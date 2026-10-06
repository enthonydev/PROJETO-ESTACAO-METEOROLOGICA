"""Testes estruturais do skeleton de firmware, sem hardware físico."""

from displays.local_display import LocalDisplay
from services.sensor_service import SensorService
from services.time_service import TimeService
from services.weather_api import WeatherStateService


class Driver:
    def __init__(self, value):
        self.value = value

    def read(self):
        return self.value


class FailingDriver:
    def read(self):
        raise RuntimeError("falha simulada")


class Display:
    def __init__(self):
        self.views = []

    def draw(self, view_model):
        self.views.append(view_model)


def test_sensor_service_isolates_driver_failure():
    snapshot = SensorService(
        {"temperature": Driver(22.5), "humidity": FailingDriver()}
    ).read()

    assert snapshot.measurements == {"temperature": 22.5, "humidity": None}
    assert snapshot.quality == {"temperature": "ok", "humidity": "error"}


def test_local_display_receives_composed_state():
    display = Display()
    state = {
        "local": {"temperature_c": 22.5},
        "clock": {"year": 2026, "month": 9, "day": 25, "hour": 0, "minute": 10},
        "external": {"condition": "clear"},
    }

    LocalDisplay(display).render(state)

    assert display.views == [state]


def test_time_service_converts_source_tuple_without_display_dependency():
    state = TimeService.to_clock_state((2026, 9, 25, 0, 10, 0, 4, 0))

    assert state.year == 2026
    assert state.weekday == 4
    assert state.hour == 0



class FailingWeatherProvider:
    def fetch(self):
        raise TimeoutError("timeout simulado")


def test_weather_service_marks_last_state_as_stale_on_expected_failure():
    service = WeatherStateService(FailingWeatherProvider())
    state = service.update()

    assert state.stale is True
    assert isinstance(service.last_error, TimeoutError)
