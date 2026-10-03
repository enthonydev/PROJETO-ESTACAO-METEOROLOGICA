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
    mqtt_broker_host: str = os.getenv("MQTT_BROKER_HOST", "localhost")
    mqtt_broker_port: int = int(os.getenv("MQTT_BROKER_PORT", "1883"))
    mqtt_subscription_topic: str = os.getenv(
        "MQTT_SUBSCRIPTION_TOPIC", "estacao/+/telemetry"
    )
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
