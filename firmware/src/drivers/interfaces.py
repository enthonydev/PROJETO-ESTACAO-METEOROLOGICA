"""Interfaces de hardware; a implementação concreta depende da validação física."""


class SensorDriver:
    """Contrato mínimo de um driver de sensor."""

    def read(self):
        raise NotImplementedError


class DisplayDriver:
    """Contrato mínimo de um driver de display."""

    def draw(self, view_model):
        raise NotImplementedError


class TimeDriver:
    """Contrato mínimo para uma fonte de data e hora."""

    def read(self):
        raise NotImplementedError
