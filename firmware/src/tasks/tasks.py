"""Tarefas cooperativas independentes da topologia física da interface."""


class SensorTask:
    def __init__(self, sensor_service):
        self.sensor_service = sensor_service

    def run_once(self):
        return self.sensor_service.read()


class SyncTask:
    """Atualiza fontes complementares de rede sem substituir sensores locais."""

    def __init__(self, weather_service, time_service):
        self.weather_service = weather_service
        self.time_service = time_service

    def run_once(self):
        return {
            "weather": self.weather_service.update(),
            "clock": self.time_service.to_clock_state(self.time_service.current()),
        }


class LocalDisplayTask:
    """Renderiza em uma única interface o estado composto fornecido pela aplicação."""

    def __init__(self, display, state_provider):
        self.display = display
        self.state_provider = state_provider

    def run_once(self):
        state = self.state_provider()
        self.display.render(state)
        return state
