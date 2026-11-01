"""Testes de integridade da interface Clima iOS recuperada do protótipo aprovado."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UI = (ROOT / "frontend" / "weather.html").read_text(encoding="utf-8")


def test_tema_ios_restaurado():
    assert 'class="ambient"' in UI
    assert 'id="weatherSwitch"' in UI
    assert 'id="chart"' in UI
    assert 'id="timeMarker"' in UI


def test_consulta_api_real_e_nao_simula_leituras():
    assert '/api/v1/stations/' in UI
    assert 'getJSON(endpoint+"/latest")' in UI
    assert 'getJSON(endpoint+"/measurements?range=24h")' in UI
    assert "Sem medições reais disponíveis" in UI
    assert "vals:[22.8" not in UI
    assert 'data-value="184"' not in UI


def test_metricas_nao_inventadas():
    assert 'id="pressureValue">--' in UI
    assert 'id="airValue">--' in UI
    assert 'id="lightValue">--' in UI
    assert 'id="rainValue">Sem dado' in UI
    assert "percentual não medido" in UI
    assert "sem previsão meteorológica" in UI
