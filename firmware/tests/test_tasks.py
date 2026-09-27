"""Testes estruturais das tasks da baseline ADR-002."""

from models.state import ClockState, WeatherState
from tasks.tasks import LocalDisplayTask, SensorTask, SyncTask


class SensorService:
    def __init__(self):
        self.calls = 0

    def read(self):
        self.calls += 1
        return "snapshot"


class WeatherService:
    def update(self):
        return WeatherState(external={"condition": "clear"})


class TimeService:
    def current(self):
        return (2026, 9, 25, 10, 30, 0, 4, 0)

    @staticmethod
    def to_clock_state(value):
        return ClockState(value[0], value[1], value[2], value[6], value[3], value[4])


class Display:
    def __init__(self):
        self.rendered = []

    def render(self, state):
        self.rendered.append(state)


def test_sensor_task_delegates_to_service():
    service = SensorService()
    assert SensorTask(service).run_once() == "snapshot"
    assert service.calls == 1


def test_sync_task_combines_complementary_services():
    result = SyncTask(WeatherService(), TimeService()).run_once()
    assert result["weather"].external["condition"] == "clear"
    assert result["clock"].hour == 10


def test_single_local_display_receives_composed_state():
    display = Display()
    state = {
        "local": {"temperature_c": 21.0},
        "clock": ClockState(2026, 9, 25, 4, 10, 30),
        "external": {"condition": "clear"},
    }
    returned = LocalDisplayTask(display, lambda: state).run_once()
    assert display.rendered == [state]
    assert returned == state
