"""Exceções de domínio dos serviços do firmware."""


class WeatherProviderError(RuntimeError):
    """Falha esperada ao consultar a fonte meteorológica externa."""
