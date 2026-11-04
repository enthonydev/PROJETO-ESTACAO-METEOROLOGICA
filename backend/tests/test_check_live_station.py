"""Validação do verificador de telemetria real sem hardware e sem rede."""
from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "check_live_station", ROOT / "scripts" / "check_live_station.py"
)
checker = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(checker)


def sample(now):
    return {
        "schema_version": "1.0",
        "timestamp": now.isoformat(),
        "quality": {"temperature": "ok", "humidity": "ok"},
        "measurements": {"temperature_c": 23.2, "humidity_pct": 85.7},
    }


def test_valid_data_is_accepted():
    now = datetime(2026, 11, 4, 20, 0, tzinfo=timezone.utc)
    assert checker.inspect_payload(sample(now), 120, now) == []


def test_stale_data_is_rejected():
    now = datetime(2026, 11, 4, 20, 0, tzinfo=timezone.utc)
    result = checker.inspect_payload(sample(now - timedelta(minutes=10)), 120, now)
    assert any("timestamp fora" in issue for issue in result)


def test_missing_values_not_counted_as_real():
    now = datetime(2026, 11, 4, 20, 0, tzinfo=timezone.utc)
    payload = sample(now)
    payload["measurements"]["temperature_c"] = None
    assert any("temperature_c nao numerico" in issue for issue in checker.inspect_payload(payload, 120, now))
