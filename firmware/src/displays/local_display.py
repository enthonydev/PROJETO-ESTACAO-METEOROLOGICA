"""Renderização da única OLED local sem acesso direto a sensores, NTP ou API."""


class LocalDisplay:
    def __init__(self, display_driver):
        self.display_driver = display_driver

    def render(self, state):
        """Recebe estado já composto e delega desenho ao driver físico."""
        self.display_driver.draw(state)
