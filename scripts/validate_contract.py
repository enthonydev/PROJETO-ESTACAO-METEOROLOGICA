"""Valida a estrutura mínima do contrato e dos exemplos de telemetria."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs/contratos/telemetria-v1.0.json"
EXAMPLES = sorted((ROOT / "docs/contratos/examples").glob("telemetry-v1.0-*.json"))

QUALITY_STATUSES = {"ok", "suspect", "invalid", "error"}
REQUIRED_MEASUREMENTS = {
    "temperature_c",
    "humidity_pct",
    "pressure_hpa",
    "air_quality_raw",
    "luminosity_pct",
    "rain_mm",
}
REQUIRED_QUALITY = {
    "temperature",
    "humidity",
    "pressure",
    "air_quality",
    "luminosity",
    "rain",
}


def fail(message: str) -> None:
    raise ValueError(message)


def validate_payload(payload: dict[str, Any], source: Path) -> None:
    required = {
        "schema_version",
        "station_id",
        "timestamp",
        "location",
        "measurements",
        "quality",
    }
    if set(payload) != required:
        fail(f"{source}: campos de primeiro nível incompatíveis")
    if payload["schema_version"] != "1.0":
        fail(f"{source}: schema_version diferente de 1.0")
    if not isinstance(payload["station_id"], str) or not payload["station_id"]:
        fail(f"{source}: station_id inválido")

    timestamp = payload["timestamp"]
    if not isinstance(timestamp, str):
        fail(f"{source}: timestamp não é texto")
    try:
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        fail(f"{source}: timestamp não está em ISO-8601: {exc}")

    location = payload["location"]
    if set(location) != {"latitude", "longitude"}:
        fail(f"{source}: localização incompatível")
    for field in ("latitude", "longitude"):
        if location[field] is not None and not isinstance(location[field], (int, float)):
            fail(f"{source}: {field} deve ser número ou nulo")

    measurements = payload["measurements"]
    if set(measurements) != REQUIRED_MEASUREMENTS:
        fail(f"{source}: conjunto de medições incompatível")
    for field, value in measurements.items():
        if value is not None and not isinstance(value, (int, float)):
            fail(f"{source}: medição {field} deve ser número ou nulo")

    quality = payload["quality"]
    if set(quality) != REQUIRED_QUALITY:
        fail(f"{source}: conjunto de estados de qualidade incompatível")
    for field, value in quality.items():
        if value not in QUALITY_STATUSES:
            fail(f"{source}: estado inválido em {field}: {value}")


def main() -> int:
    if not SCHEMA_PATH.is_file():
        print(f"Arquivo ausente: {SCHEMA_PATH}", file=sys.stderr)
        return 1
    json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if not EXAMPLES:
        print("Nenhum exemplo de telemetria encontrado", file=sys.stderr)
        return 1
    for path in EXAMPLES:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            fail(f"{path}: payload deve ser objeto JSON")
        validate_payload(payload, path)
        print(f"OK: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
