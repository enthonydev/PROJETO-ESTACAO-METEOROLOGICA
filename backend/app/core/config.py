"""Configuração mínima do backend por variáveis de ambiente."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Estação Meteorológica")
    mqtt_topic_pattern: str = os.getenv(
        "MQTT_TOPIC_PATTERN", "estacao/<station_id>/telemetry"
    )
    database_url: str | None = os.getenv("DATABASE_URL")


settings = Settings()
