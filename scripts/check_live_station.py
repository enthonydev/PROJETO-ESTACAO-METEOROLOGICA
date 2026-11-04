"""Verifica se o backend possui telemetria recente da estacao FISICA.

Nao cria dados, nao usa fixtures, nao declara MQTT validado so por HTTP.
Exit 0: API devolveu medida recente e numerica.
Exit 1: falta leitura real/recente ou houve erro de conexao.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen


def inspect_payload(payload: dict, max_age_seconds: int, now: datetime | None = None) -> list[str]:
    problems = []
    if payload.get("schema_version") != "1.0":
        problems.append("schema_version diferente de 1.0")
    ts = payload.get("timestamp")
    try:
        observed = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        if observed.tzinfo is None:
            problems.append("timestamp sem fuso horario")
        else:
            age = ((now or datetime.now(timezone.utc)) - observed).total_seconds()
            if age < -60 or age > max_age_seconds:
                problems.append(f"timestamp fora da janela: {age:.0f} s")
    except (ValueError, TypeError, AttributeError):
        problems.append("timestamp invalido")

    m = payload.get("measurements") or {}
    quality = payload.get("quality") or {}
    for key, q in (("temperature_c", "temperature"), ("humidity_pct", "humidity")):
        value = m.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            problems.append(f"{key} nao numerico")
        if quality.get(q) != "ok":
            problems.append(f"qualidade {q} nao esta ok")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api", default="http://127.0.0.1:8000")
    parser.add_argument("--station", default="estacao-esp32-real")
    parser.add_argument("--max-age", type=int, default=120)
    args = parser.parse_args()
    uri = (
        args.api.rstrip("/")
        + "/api/v1/stations/"
        + quote(args.station, safe="")
        + "/latest"
    )
    try:
        with urlopen(uri, timeout=7) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        print(f"[PENDENTE] Nao foi possivel consultar leitura real: {exc}")
        return 1
    issues = inspect_payload(payload, args.max_age)
    if issues:
        print("[PENDENTE] API respondeu, mas:", "; ".join(issues))
        return 1
    m = payload["measurements"]
    print(f"[OK] {args.station}: temp={m['temperature_c']} C, umidade={m['humidity_pct']} %")
    print(f"Timestamp UTC: {payload['timestamp']}. Verificacao via API, origem fisica deve ser confirmada em bancada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
