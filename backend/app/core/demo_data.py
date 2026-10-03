"""Dados sintéticos de desenvolvimento para executar a API sem hardware."""

from datetime import datetime, timedelta, timezone

from app.schemas.telemetry import Location, Measurements, Quality, TelemetryPayload


def build_demo_payloads(station_id: str = "estacao-01") -> list[TelemetryPayload]:
    """Gera histórico determinístico, identificado como dado de demonstração."""
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    payloads: list[TelemetryPayload] = []

    for index in range(72):
        measured_at = now - timedelta(hours=71 - index)
        daylight = max(0.0, 1 - abs((measured_at.hour - 12) / 7))
        temperature = 21.8 + daylight * 5.4 + ((index % 5) - 2) * 0.12
        humidity = 74 - daylight * 18 + ((index % 4) - 1.5) * 0.6
        pressure = 1012 + ((index % 9) - 4) * 0.25
        air_quality = 176 + daylight * 15 + ((index % 6) - 2.5) * 1.2
        luminosity = min(100.0, max(0.0, daylight * 88))

        payloads.append(
            TelemetryPayload(
                schema_version="1.0",
                station_id=station_id,
                timestamp=measured_at,
                location=Location(latitude=None, longitude=None),
                measurements=Measurements(
                    temperature_c=round(temperature, 1),
                    humidity_pct=round(humidity),
                    pressure_hpa=round(pressure),
                    air_quality_raw=round(air_quality),
                    luminosity_pct=round(luminosity),
                    rain_mm=None,
                ),
                quality=Quality(
                    temperature="ok",
                    humidity="ok",
                    pressure="ok",
                    air_quality="suspect",
                    luminosity="ok",
                    rain="error",
                ),
            )
        )

    return payloads
