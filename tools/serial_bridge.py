"""Ponte experimental: ESP32 Arduino USB serial -> ingestao HTTP local do FastAPI.

Nao substitui MQTT e nao preenche campos sem medicao valida.
Requer: pip install pyserial
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DHT_RE = re.compile(
    r"^Temperatura:\s*(-?\d+(?:\.\d+)?)\s*C\s*\|\s*Umidade:\s*(\d+(?:\.\d+)?)\s*%$"
)
CHUVA_RE = re.compile(r"^Chuva:\s*(DETECTADA|NAO DETECTADA)$")
CHUVA_DIAG_RE = re.compile(r"^\[DIAGNOSTICO\] Chuva GPIO17:\s*(HIGH|LOW)")
LUZ_RE = re.compile(r"^Luminosidade:\s*(CLARO|ESCURO)$")


def parse_line(line: str) -> dict | None:
    """Extrai somente valores presentes no log Arduino validado."""
    line = line.strip()
    match = DHT_RE.match(line)
    if match:
        temperature = float(match.group(1))
        humidity = float(match.group(2))
        if not (-40 <= temperature <= 80 and 0 <= humidity <= 100):
            return None
        return {"type": "dht", "temperature_c": temperature, "humidity_pct": humidity}
    match = CHUVA_RE.match(line)
    if match:
        return {"type": "rain", "detected": match.group(1) == "DETECTADA"}
    match = CHUVA_DIAG_RE.match(line)
    if match:
        return {"type": "rain", "detected": match.group(1) == "LOW"}
    match = LUZ_RE.match(line)
    if match:
        return {"type": "light", "dark": match.group(1) == "ESCURO"}
    return None


def make_payload(station_id: str, reading: dict) -> dict:
    """Contrato v1.0: somente DHT possui grandezas quantitativas validadas."""
    return {
        "schema_version": "1.0",
        "station_id": station_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "location": {"latitude": None, "longitude": None},
        "measurements": {
            "temperature_c": reading["temperature_c"],
            "humidity_pct": reading["humidity_pct"],
            "pressure_hpa": None,
            "air_quality_raw": None,
            "luminosity_pct": None,
            "rain_mm": None,
        },
        "quality": {
            "temperature": "ok",
            "humidity": "ok",
            "pressure": "error",
            "air_quality": "error",
            "luminosity": "error",
            "rain": "error",
        },
    }


def send_payload(api_url: str, payload: dict) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(
        api_url.rstrip("/") + "/api/v1/telemetry",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=5) as response:
        if response.status != 201:
            raise RuntimeError(f"Resposta HTTP inesperada: {response.status}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True, help="Porta ESP32, ex.: COM7")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--api", default="http://127.0.0.1:8000")
    parser.add_argument("--station-id", default="estacao-esp32-real")
    args = parser.parse_args()

    try:
        import serial
    except ImportError:
        print("Instale pyserial: python -m pip install pyserial", file=sys.stderr)
        return 2

    print(f"Conectando ESP32 em {args.port} ({args.baud} baud)...")
    print("Feche o Monitor Serial do Arduino IDE antes de iniciar esta ponte.")
    try:
        with serial.Serial(args.port, args.baud, timeout=1) as device:
            # Algumas placas ESP32 reiniciam ao abrir a porta USB serial.
            time.sleep(2)
            device.reset_input_buffer()
            while True:
                raw = device.readline()
                if not raw:
                    continue
                line = raw.decode("utf-8", errors="replace").strip()
                item = parse_line(line)
                if item is None:
                    continue
                if item["type"] == "rain":
                    print("Chuva digital:", "SIM" if item["detected"] else "NAO")
                elif item["type"] == "light":
                    print("Luz digital:", "ESCURO" if item["dark"] else "CLARO")
                elif item["type"] == "dht":
                    payload = make_payload(args.station_id, item)
                    try:
                        send_payload(args.api, payload)
                        print(
                            f"Enviado: {item['temperature_c']:.1f} C; "
                            f"{item['humidity_pct']:.1f}% UR"
                        )
                    except (HTTPError, URLError, TimeoutError, RuntimeError) as exc:
                        print(f"Falha HTTP: {exc}", file=sys.stderr)
    except (OSError, serial.SerialException) as exc:
        print(f"Falha ao abrir/ler porta serial: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nPonte encerrada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
