"""Renderização da tela meteorológica sem acesso a API ou sensores."""


class WeatherDisplay:
    def __init__(self, display_driver):
        self.display_driver = display_driver

    def render(self, state):
        view_model = {
            "external": state.external,
            "local": state.local,
            "stale": state.stale,
        }
        self.display_driver.draw(view_model)
