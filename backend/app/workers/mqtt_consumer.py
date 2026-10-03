"""Worker MQTT do backend.

Executar separadamente do servidor HTTP:

    PYTHONPATH=backend python -m app.workers.mqtt_consumer
"""

import logging

import paho.mqtt.client as mqtt

from app.api.dependencies import get_measurement_repository
from app.core.config import settings
from app.services.mqtt_ingestion import InvalidMqttMessageError, process_mqtt_message


logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        client.subscribe(settings.mqtt_subscription_topic)
        logger.info("Assinatura MQTT ativa em %s", settings.mqtt_subscription_topic)
    else:
        logger.error("Falha na conexão MQTT: %s", reason_code)


def on_message(client, userdata, message):
    repository = get_measurement_repository()

    try:
        process_mqtt_message(message.topic, message.payload, repository)
        logger.info("Telemetria recebida em %s", message.topic)
    except InvalidMqttMessageError as exc:
        logger.warning("Mensagem MQTT rejeitada em %s: %s", message.topic, exc)


def main() -> None:
    logging.basicConfig(level=settings.log_level)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
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
