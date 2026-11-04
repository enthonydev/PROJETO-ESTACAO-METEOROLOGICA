"""Worker MQTT do backend.

Executar separadamente do servidor HTTP:

    PYTHONPATH=backend python -m app.workers.mqtt_consumer
"""

import json
import logging

import paho.mqtt.client as mqtt

from app.api.dependencies import get_measurement_repository
from app.repositories.digital_states import get_digital_states_repository
from app.schemas.digital import DigitalState
from pydantic import ValidationError
from app.core.config import settings
from app.services.mqtt_ingestion import InvalidMqttMessageError, process_mqtt_message


logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        client.subscribe(settings.mqtt_subscription_topic)
        client.subscribe("estacao/+/digital")
        logger.info("Assinatura MQTT ativa em %s", settings.mqtt_subscription_topic)
    else:
        logger.error("Falha na conexão MQTT: %s", reason_code)


def on_message(client, userdata, message):
    if message.topic.endswith("/digital"):
        try:
            parts = message.topic.split("/")
            if len(parts) != 3 or parts[0] != "estacao" or not parts[1]:
                raise ValueError("Topico digital invalido")
            if len(message.payload) > 1024:
                raise ValueError("Payload digital excede o limite")
            payload = DigitalState.model_validate(json.loads(message.payload))
            if payload.station_id != parts[1]:
                raise ValueError("station_id nao corresponde ao topico")
            get_digital_states_repository().add(payload)
            logger.info("Estado digital recebido em %s", message.topic)
        except (ValueError, UnicodeDecodeError, ValidationError) as exc:
            logger.warning("Estado digital rejeitado em %s: %s", message.topic, exc)
        return

    repository = get_measurement_repository()
    try:
        process_mqtt_message(message.topic, message.payload, repository)
        logger.info("Telemetria recebida em %s", message.topic)
    except InvalidMqttMessageError as exc:
        logger.warning("Mensagem MQTT rejeitada em %s: %s", message.topic, exc)


def main() -> None:
    logging.basicConfig(level=settings.log_level)

    if not settings.database_url:
        raise RuntimeError(
            "DATABASE_URL é obrigatória para o worker MQTT separado. "
            "O repositório em memória não é compartilhado com o processo da API."
        )

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if settings.mqtt_username and settings.mqtt_password:
        client.username_pw_set(settings.mqtt_username, settings.mqtt_password)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(
        settings.mqtt_broker_host,
        settings.mqtt_broker_port,
        keepalive=60,
    )
    client.loop_forever()


if __name__ == "__main__":
    main()
