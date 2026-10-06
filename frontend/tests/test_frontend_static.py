from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
HTML = (ROOT / "frontend" / "index.html").read_text(encoding="utf-8")
JS_FILES = list((ROOT / "frontend" / "src").glob("*.js"))
JS = "\n".join(path.read_text(encoding="utf-8") for path in JS_FILES)
CSS = (ROOT / "frontend" / "src" / "styles.css").read_text(encoding="utf-8")


def test_arquivos_principais_presentes():
    assert "<main id=\"dashboard\"" in HTML
    assert 'id="historyChart"' in HTML
    assert 'id="qualityList"' in HTML
    assert 'id="exportButton"' in HTML


def test_metricas_do_contrato_referenciadas():
    for field in [
        "temperature_c",
        "humidity_pct",
        "pressure_hpa",
        "air_quality_raw",
        "luminosity_pct",
        "rain_mm",
    ]:
        assert field in JS


def test_chuva_nao_e_inventada():
    assert 'measurements.rain_mm === null' in JS
    assert 'sensor experimental' in JS


def test_modo_mock_explicitamente_identificado():
    assert "Boolean(demoMode)" in JS
    assert "não representam medições físicas" in JS
    assert "/api/v1/stations/" in JS


def test_controles_acessiveis():
    assert 'aria-pressed="true"' in HTML
    assert 'aria-live="polite"' in HTML
    assert 'aria-busy="true"' in HTML
    assert ":focus-visible" in CSS


def test_sem_dependencias_frontend_externas():
    assert "https://cdn." not in HTML
    assert "unpkg.com" not in HTML
    assert "cdnjs" not in HTML


def test_frontend_modularizado():
    assert 'type="module"' in HTML
    for module in ["config.js", "state.js", "demo-data.js"]:
        assert (ROOT / "frontend" / "src" / module).is_file()


def test_ids_referenciados_no_js_existem_no_html():
    ids = set(re.findall(r'id="([^"]+)"', HTML))
    for match in re.findall(r'getElementById\("([^"]+)"\)', JS):
        assert match in ids, f"ID usado no JS não existe no HTML: {match}"
