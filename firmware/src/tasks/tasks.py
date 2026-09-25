"""Tarefas cooperativas como unidades independentes de atualização."""


class SensorTask:
    def __init__(self, sensor_service):
        self.sensor_service = sensor_service

    def run_once(self):
        return self.sensor_service.read()


class SyncTask:
    def __init__(self, weather_service, time_service):
        self.weather_service = weather_service
        self.time_service = time_service

    def run_once(self):
        return {
            "weather": self.weather_service.update(),
            "clock": self.time_service.to_clock_state(self.time_service.current()),
        }


class WeatherTask:
    def __init__(self, display, state_provider):
        self.display = display
        self.state_provider = state_provider

    def run_once(self):
        self.display.render(self.state_provider())


class ClockTask:
    def __init__(self, display, state_provider):
        self.display = display
        self.state_provider = state_provider

    def run_once(self):
        self.display.render(self.state_provider())
