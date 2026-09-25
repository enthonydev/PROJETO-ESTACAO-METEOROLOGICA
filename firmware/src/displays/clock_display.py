"""Renderização de data e hora sem sincronização NTP direta."""


class ClockDisplay:
    def __init__(self, display_driver):
        self.display_driver = display_driver

    def render(self, state):
        view_model = {
            "year": state.year,
            "month": state.month,
            "day": state.day,
            "weekday": state.weekday,
            "hour": state.hour,
            "minute": state.minute,
        }
        self.display_driver.draw(view_model)
