"""Testes unitários sem necessidade do ESP32 nem conexão de rede."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("serial_bridge", ROOT / "tools" / "serial_bridge.py")
bridge = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(bridge)


def test_parse_dht_real():
    assert bridge.parse_line("Temperatura: 23.2 C | Umidade: 85.7 %") == {
        "type": "dht", "temperature_c": 23.2, "humidity_pct": 85.7
    }


def test_parse_digital_states():
    assert bridge.parse_line("Chuva: DETECTADA") == {"type": "rain", "detected": True}
    assert bridge.parse_line("Chuva: NAO DETECTADA") == {"type": "rain", "detected": False}
    assert bridge.parse_line("[DIAGNOSTICO] Chuva GPIO17: HIGH | Interpretacao: SEM AGUA DETECTADA") == {
        "type": "rain", "detected": False
    }
    assert bridge.parse_line("Luminosidade: CLARO") == {"type": "light", "dark": False}
    assert bridge.parse_line("Luminosidade: ESCURO") == {"type": "light", "dark": True}


def test_nao_inventa_medidas():
    p = bridge.make_payload("estacao-esp32-real", {
        "temperature_c": 23.2, "humidity_pct": 85.7
    })
    assert p["schema_version"] == "1.0"
    assert p["measurements"]["rain_mm"] is None
    assert p["measurements"]["luminosity_pct"] is None
    assert p["measurements"]["pressure_hpa"] is None
    assert p["measurements"]["air_quality_raw"] is None
    assert p["quality"]["rain"] == "error"
    assert p["quality"]["luminosity"] == "error"


def test_rejeita_dado_invalido():
    assert bridge.parse_line("Temperatura: 22.0 C | Umidade: 122.0 %") is None
