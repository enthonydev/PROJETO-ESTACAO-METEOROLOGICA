"""Testes estruturais do skeleton de firmware, sem hardware físico."""

from displays.clock_display import ClockDisplay
from displays.weather_display import WeatherDisplay
from models.state import ClockState, WeatherState
from services.sensor_service import SensorService
from services.time_service import TimeService


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


def test_weather_display_receives_processed_state():
    display = Display()
    state = WeatherState(external={"condition": "clear"}, local={"temperature_c": 22.5})

    WeatherDisplay(display).render(state)

    assert display.views == [
        {
            "external": {"condition": "clear"},
            "local": {"temperature_c": 22.5},
            "stale": False,
        }
    ]


def test_clock_display_receives_resolved_time():
    display = Display()
    state = ClockState(2026, 9, 25, 4, 0, 10)

    ClockDisplay(display).render(state)

    assert display.views[0]["year"] == 2026
    assert display.views[0]["minute"] == 10


def test_time_service_converts_source_tuple_without_ntp_logic_in_display():
    state = TimeService.to_clock_state((2026, 9, 25, 0, 10, 0, 4, 0))

    assert state.year == 2026
    assert state.weekday == 4
    assert state.hour == 0
