"""Processamento de mensagens MQTT de telemetria."""

import json
import re

from app.repositories.measurements import MeasurementRepository
from app.services.telemetry_validation import InvalidTelemetryError, validate_telemetry


TOPIC_PATTERN = re.compile(r"^estacao/(?P<station_id>[^/]+)/telemetry$")


class InvalidMqttMessageError(ValueError):
    """Indica tópico ou payload MQTT incompatível com o contrato."""


def process_mqtt_message(
    topic: str,
    payload_bytes: bytes,
    repository: MeasurementRepository,
):
    """Valida tópico, JSON e contrato antes de persistir a telemetria."""
    match = TOPIC_PATTERN.fullmatch(topic)
    if not match:
        raise InvalidMqttMessageError("Tópico MQTT inválido")

    try:
        raw = json.loads(payload_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InvalidMqttMessageError("Payload MQTT não é JSON UTF-8 válido") from exc

    try:
        telemetry = validate_telemetry(raw)
    except InvalidTelemetryError as exc:
        raise InvalidMqttMessageError("Payload MQTT incompatível com o contrato") from exc

    if telemetry.station_id != match.group("station_id"):
        raise InvalidMqttMessageError(
            "station_id do payload não corresponde ao tópico MQTT"
        )

    repository.add(telemetry)
    return telemetry
