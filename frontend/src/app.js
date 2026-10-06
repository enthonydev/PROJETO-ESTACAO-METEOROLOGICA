import { AUTO_REFRESH_MS, USE_MOCK_DATA, metricConfig } from "./config.js";
import { fetchHistory, fetchLatest, validateTelemetry } from "./api.js";
import { renderChart } from "./chart.js";
import { buildMockLatest, getMockHistory } from "./demo-data.js";
import { state } from "./state.js";

const demoMode = new URLSearchParams(window.location.search).get("demo");
const USING_DEMO_DATA = USE_MOCK_DATA || Boolean(demoMode);

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) element.textContent = value;
}

function formatDateTime(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Data indisponível";

  return new Intl.DateTimeFormat("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  }).format(date);
}

function metricLabel(value) {
  return value === null || value === undefined ? "--" : String(value);
}

function setBusy(isBusy) {
  document.getElementById("dashboard").setAttribute("aria-busy", String(isBusy));

  document.querySelectorAll(".range-btn, .metric-btn, #exportButton, #refreshButton").forEach(button => {
    button.disabled = isBusy;
  });
}

function setConnectionState(kind, label) {
  document.getElementById("connectionDot").dataset.state = kind;
  setText("connectionLabel", label);
}

function setNotice(message, stateName = "neutral", canRetry = false) {
  const notice = document.getElementById("systemNotice");
  const retry = document.getElementById("retryButton");

  notice.dataset.state = stateName;
  setText("noticeText", message);
  retry.hidden = !canRetry;
}

function deriveDataState(quality) {
  const statuses = Object.values(quality);

  if (statuses.every(status => status === "ok")) return "Válido";
  if (statuses.some(status => status === "error" || status === "invalid")) return "Parcial";
  if (statuses.some(status => status === "suspect")) return "Com ressalvas";

  return "Indefinido";
}

function renderFreshness(timestamp) {
  const date = new Date(timestamp);

  if (Number.isNaN(date.getTime())) {
    setText("freshnessLabel", "Atualidade: indisponível");
    return;
  }

  const ageMinutes = Math.max(0, Math.floor((Date.now() - date.getTime()) / 60_000));

  if (ageMinutes < 2) setText("freshnessLabel", "Atualidade: agora");
  else if (ageMinutes < 10) setText("freshnessLabel", `Atualidade: ${ageMinutes} min`);
  else if (ageMinutes < 60) setText("freshnessLabel", `Atualidade: atrasada (${ageMinutes} min)`);
  else setText("freshnessLabel", "Atualidade: leitura antiga");
}

function renderLocation(location) {
  const lat = location?.latitude;
  const lon = location?.longitude;

  if (!Number.isFinite(lat) || !Number.isFinite(lon)) {
    setText("statusLocation", "Não informada");
    return;
  }

  setText("statusLocation", `${lat.toFixed(4)}, ${lon.toFixed(4)}`);
}

function renderLatest(rawPayload) {
  const payload = validateTelemetry(rawPayload);
  state.latest = payload;

  const measurements = payload.measurements;
  const stationLabel = payload.station_id
    .replaceAll("-", " ")
    .replace(/\b\w/g, char => char.toUpperCase());

  setText("stationName", stationLabel);
  setText("temperatureValue", metricLabel(measurements.temperature_c));
  setText("humidityValue", metricLabel(measurements.humidity_pct));
  setText("pressureValue", metricLabel(measurements.pressure_hpa));
  setText("airQualityValue", metricLabel(measurements.air_quality_raw));
  setText("luminosityValue", metricLabel(measurements.luminosity_pct));

  if (measurements.rain_mm === null || payload.quality.rain !== "ok") {
    setText("rainValue", "Sem dado");
    setText("rainUnit", "sensor experimental");
  } else {
    setText("rainValue", metricLabel(measurements.rain_mm));
    setText("rainUnit", "mm");
  }

  setText("lastUpdate", `Última atualização: ${formatDateTime(payload.timestamp)}`);
  setText("statusStation", USING_DEMO_DATA ? "Demonstração" : "Operacional");
  setText("statusData", deriveDataState(payload.quality));
  setText("statusSource", USING_DEMO_DATA ? "Simulação" : "API REST");
  setText("statusUpdated", formatDateTime(payload.timestamp));
  setText("statusSchema", payload.schema_version);
  setText(
    "temperatureNote",
    USING_DEMO_DATA ? "Leitura simulada para desenvolvimento da interface" : "Leitura recebida da API"
  );

  renderFreshness(payload.timestamp);
  renderLocation(payload.location);
  renderQuality(payload.quality);
}

function renderQuality(quality) {
  const labels = {
    temperature: "Temperatura",
    humidity: "Umidade",
    pressure: "Pressão",
    air_quality: "Ar",
    luminosity: "Luminosidade",
    rain: "Chuva"
  };

  const statusLabels = {
    ok: "ok",
    suspect: "atenção",
    invalid: "inválido",
    error: "sem leitura"
  };

  const container = document.getElementById("qualityList");
  container.innerHTML = "";

  Object.entries(quality).forEach(([key, status]) => {
    const tag = document.createElement("span");
    tag.className = "quality-tag";
    tag.dataset.status = status;
    tag.textContent = `${labels[key] ?? key} · ${statusLabels[status] ?? status}`;
    container.appendChild(tag);
  });
}

async function loadLatest() {
  if (demoMode === "error") throw new Error("Falha simulada da API para teste da interface.");

  if (USING_DEMO_DATA) {
    renderLatest(buildMockLatest(demoMode));
    return;
  }

  renderLatest(await fetchLatest(state.station));
}

async function loadHistory(range, metric) {
  if (demoMode === "error") throw new Error("Falha simulada da API para teste da interface.");

  if (USING_DEMO_DATA) {
    state.history = getMockHistory(range, metric, demoMode);
    renderChart(state.history, range, metric);
    return;
  }

  const data = await fetchHistory(state.station, range);
  const items = Array.isArray(data) ? data : data.items ?? [];

  state.history = items
    .map(item => item?.[metric] ?? item?.measurements?.[metric])
    .filter(Number.isFinite);

  renderChart(state.history, range, metric);
}

function buildCsv() {
  const config = metricConfig[state.metric];
  const rows = [
    ["periodo", "metrica", "unidade", "indice", "valor"],
    ...state.history.map((value, index) => [state.range, state.metric, config.unit, index + 1, value])
  ];

  return rows
    .map(row => row.map(value => `"${String(value).replaceAll('"', '""')}"`).join(","))
    .join("\n");
}

function exportCsv() {
  if (!state.history.length) {
    setNotice("Não há histórico para exportar neste período.", "neutral", false);
    return;
  }

  const blob = new Blob([buildCsv()], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");

  anchor.href = url;
  anchor.download = `${state.station}-${state.metric}-${state.range}.csv`;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

function renderClock() {
  const now = new Date();
  const label = new Intl.DateTimeFormat("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit"
  }).format(now);

  const element = document.getElementById("currentTime");
  element.textContent = label;
  element.dateTime = now.toISOString();
}

function renderOfflineState() {
  if (USING_DEMO_DATA) return;

  setConnectionState("offline", "Offline");
  setNotice("Sem conexão com a rede. Os últimos dados carregados permanecem na tela.", "offline", true);
  setText("statusStation", "Offline");
}

function handleError(error) {
  console.error(error);
  setConnectionState("error", "Indisponível");
  setNotice(error.message || "Não foi possível atualizar o painel.", "error", true);
  setText("statusStation", "Sem conexão");
  setText("statusData", state.latest ? deriveDataState(state.latest.quality) : "Não disponível");
  setText("statusSource", USING_DEMO_DATA ? "Simulação" : "API REST");
}

async function refreshDashboard() {
  setBusy(true);
  setConnectionState("loading", "Carregando");
  setNotice("Atualizando leituras...", "loading", false);

  try {
    await Promise.all([
      loadLatest(),
      loadHistory(state.range, state.metric)
    ]);

    state.lastSuccessfulRefresh = new Date();

    if (USING_DEMO_DATA) {
      setConnectionState("warning", "Simulação");
      setNotice(
        "Modo de demonstração: os valores desta tela são simulados e não representam medições físicas.",
        "mock",
        false
      );
    } else {
      setConnectionState("ok", "Online");
      setNotice("Dados atualizados pela API da estação.", "neutral", false);
    }
  } catch (error) {
    handleError(error);
  } finally {
    setBusy(false);
  }
}

async function changeHistory() {
  setBusy(true);

  try {
    await loadHistory(state.range, state.metric);
  } catch (error) {
    handleError(error);
  } finally {
    setBusy(false);
  }
}

document.querySelectorAll(".range-btn").forEach(button => {
  button.addEventListener("click", async () => {
    document.querySelectorAll(".range-btn").forEach(item => item.classList.remove("active"));
    button.classList.add("active");
    state.range = button.dataset.range;
    await changeHistory();
  });
});

document.querySelectorAll(".metric-btn").forEach(button => {
  button.addEventListener("click", async () => {
    document.querySelectorAll(".metric-btn").forEach(item => {
      const active = item === button;
      item.classList.toggle("active", active);
      item.setAttribute("aria-pressed", String(active));
    });

    state.metric = button.dataset.metric;
    await changeHistory();
  });
});

document.getElementById("retryButton").addEventListener("click", refreshDashboard);
document.getElementById("refreshButton").addEventListener("click", refreshDashboard);
document.getElementById("exportButton").addEventListener("click", exportCsv);

window.addEventListener("offline", renderOfflineState);
window.addEventListener("online", () => {
  if (!USING_DEMO_DATA) refreshDashboard();
});

renderClock();
setInterval(renderClock, 1000);
setInterval(() => {
  if (!document.hidden) refreshDashboard();
}, AUTO_REFRESH_MS);

refreshDashboard();
