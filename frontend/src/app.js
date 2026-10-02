const API_BASE = "";
const USE_MOCK_DATA = true;

const state = {
  range: "24h",
  station: "estacao-01",
  latest: null,
  history: []
};

const mockLatest = {
  schema_version: "1.0",
  station_id: "estacao-01",
  timestamp: new Date().toISOString(),
  location: { latitude: null, longitude: null },
  measurements: {
    temperature_c: 24.8,
    humidity_pct: 63,
    pressure_hpa: 1012,
    air_quality_raw: 184,
    luminosity_pct: 72,
    rain_mm: null
  },
  quality: {
    temperature: "ok",
    humidity: "ok",
    pressure: "ok",
    air_quality: "suspect",
    luminosity: "ok",
    rain: "error"
  }
};

const historySets = {
  "24h": [22.8,22.4,22.1,21.9,21.8,22.2,23.1,24.4,25.6,26.4,27.1,27.5,27.2,26.8,26.3,25.9,25.5,25.2,24.9,24.7,24.5,24.4,24.6,24.8],
  "7d": [23.6,24.1,23.9,25.0,24.5,24.7,24.8],
  "30d": [23.1,23.4,23.8,24.0,24.3,24.2,24.5,24.8,25.1,24.7,24.5,24.9,25.2,25.4,25.0,24.6,24.3,24.1,24.4,24.8,25.1,25.3,25.0,24.7,24.5,24.4,24.6,24.7,24.8,24.8]
};

const requiredMeasurementKeys = [
  "temperature_c",
  "humidity_pct",
  "pressure_hpa",
  "air_quality_raw",
  "luminosity_pct",
  "rain_mm"
];

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
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
  document.querySelectorAll(".range-btn").forEach(button => {
    button.disabled = isBusy;
  });
}

function setConnectionState(kind, label) {
  const dot = document.getElementById("connectionDot");
  dot.dataset.state = kind;
  setText("connectionLabel", label);
}

function setNotice(message, stateName = "neutral", canRetry = false) {
  const notice = document.getElementById("systemNotice");
  const retry = document.getElementById("retryButton");
  notice.dataset.state = stateName;
  setText("noticeText", message);
  retry.hidden = !canRetry;
}

function validateTelemetry(payload) {
  if (!payload || typeof payload !== "object") {
    throw new Error("Resposta de telemetria ausente.");
  }

  if (payload.schema_version !== "1.0") {
    throw new Error("Versão de telemetria incompatível.");
  }

  if (!payload.station_id || typeof payload.station_id !== "string") {
    throw new Error("Identificação da estação ausente.");
  }

  if (!payload.measurements || !payload.quality) {
    throw new Error("Telemetria incompleta.");
  }

  const missingKey = requiredMeasurementKeys.find(key => !(key in payload.measurements));
  if (missingKey) {
    throw new Error(`Métrica ausente no payload: ${missingKey}`);
  }

  return payload;
}

function deriveDataState(quality) {
  const statuses = Object.values(quality);

  if (statuses.every(status => status === "ok")) return "Válido";
  if (statuses.some(status => status === "error" || status === "invalid")) return "Parcial";
  if (statuses.some(status => status === "suspect")) return "Com ressalvas";

  return "Indefinido";
}

function renderLatest(rawPayload) {
  const payload = validateTelemetry(rawPayload);
  state.latest = payload;

  const m = payload.measurements;
  const stationLabel = payload.station_id
    .replaceAll("-", " ")
    .replace(/\b\w/g, char => char.toUpperCase());

  setText("stationName", stationLabel);
  setText("temperatureValue", metricLabel(m.temperature_c));
  setText("humidityValue", metricLabel(m.humidity_pct));
  setText("pressureValue", metricLabel(m.pressure_hpa));
  setText("airQualityValue", metricLabel(m.air_quality_raw));
  setText("luminosityValue", metricLabel(m.luminosity_pct));

  if (m.rain_mm === null || payload.quality.rain !== "ok") {
    setText("rainValue", "Sem dado");
    setText("rainUnit", "sensor experimental");
  } else {
    setText("rainValue", metricLabel(m.rain_mm));
    setText("rainUnit", "mm");
  }

  setText("lastUpdate", `Última atualização: ${formatDateTime(payload.timestamp)}`);
  setText("statusStation", USE_MOCK_DATA ? "Demonstração" : "Operacional");
  setText("statusData", deriveDataState(payload.quality));
  setText("statusSource", USE_MOCK_DATA ? "Simulação" : "API REST");
  setText("statusUpdated", formatDateTime(payload.timestamp));
  setText(
    "temperatureNote",
    USE_MOCK_DATA ? "Leitura simulada para desenvolvimento da interface" : "Leitura recebida da estação"
  );

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

function showChartEmpty(show) {
  document.getElementById("chartEmpty").hidden = !show;
  document.getElementById("temperatureChart").hidden = show;
}

function renderChart(values, range) {
  const cleanValues = values.filter(Number.isFinite);

  if (cleanValues.length < 2) {
    showChartEmpty(true);
    setText("chartMin", "--");
    setText("chartAvg", "--");
    setText("chartMax", "--");
    return;
  }

  showChartEmpty(false);

  const svg = document.getElementById("temperatureChart");
  const width = 760;
  const height = 280;
  const pad = { top: 20, right: 16, bottom: 32, left: 38 };

  const min = Math.min(...cleanValues);
  const max = Math.max(...cleanValues);
  const avg = cleanValues.reduce((sum, value) => sum + value, 0) / cleanValues.length;
  const spread = Math.max(max - min, 2);
  const yMin = min - spread * 0.25;
  const yMax = max + spread * 0.25;

  setText("chartMin", `${min.toFixed(1)}°`);
  setText("chartAvg", `${avg.toFixed(1)}°`);
  setText("chartMax", `${max.toFixed(1)}°`);

  const x = index => pad.left + (index / Math.max(cleanValues.length - 1, 1)) * (width - pad.left - pad.right);
  const y = value => pad.top + ((yMax - value) / (yMax - yMin)) * (height - pad.top - pad.bottom);

  const linePoints = cleanValues.map((value, index) => `${x(index)},${y(value)}`).join(" ");
  const areaPoints = `${pad.left},${height - pad.bottom} ${linePoints} ${width - pad.right},${height - pad.bottom}`;

  const yTicks = Array.from({ length: 4 }, (_, index) => yMin + ((yMax - yMin) / 3) * index);
  const labels = range === "24h"
    ? ["00h", "06h", "12h", "18h", "Agora"]
    : range === "7d"
      ? ["7d", "5d", "3d", "1d", "Hoje"]
      : ["30d", "21d", "14d", "7d", "Hoje"];

  const grid = yTicks.map(tick => {
    const yy = y(tick);
    return `
      <line class="chart-grid" x1="${pad.left}" x2="${width - pad.right}" y1="${yy}" y2="${yy}" />
      <text class="chart-label" x="0" y="${yy + 4}">${tick.toFixed(0)}°</text>
    `;
  }).join("");

  const xLabels = labels.map((label, index) => {
    const xx = pad.left + (index / (labels.length - 1)) * (width - pad.left - pad.right);
    const anchor = index === 0 ? "start" : index === labels.length - 1 ? "end" : "middle";
    return `<text class="chart-label" text-anchor="${anchor}" x="${xx}" y="${height - 6}">${label}</text>`;
  }).join("");

  svg.innerHTML = `
    ${grid}
    <polygon class="chart-area" points="${areaPoints}" />
    <polyline class="chart-line" points="${linePoints}" />
    ${xLabels}
  `;
}

async function loadLatest() {
  if (USE_MOCK_DATA) {
    renderLatest(mockLatest);
    return;
  }

  const response = await fetch(`${API_BASE}/api/v1/stations/${state.station}/latest`, {
    headers: { Accept: "application/json" }
  });

  if (!response.ok) {
    throw new Error(`Falha ao carregar leitura atual (HTTP ${response.status}).`);
  }

  renderLatest(await response.json());
}

async function loadHistory(range) {
  if (USE_MOCK_DATA) {
    state.history = historySets[range] ?? [];
    renderChart(state.history, range);
    return;
  }

  const response = await fetch(
    `${API_BASE}/api/v1/stations/${state.station}/measurements?range=${encodeURIComponent(range)}`,
    { headers: { Accept: "application/json" } }
  );

  if (!response.ok) {
    throw new Error(`Falha ao carregar histórico (HTTP ${response.status}).`);
  }

  const data = await response.json();
  const items = Array.isArray(data) ? data : data.items ?? [];
  state.history = items
    .map(item => item?.temperature_c ?? item?.measurements?.temperature_c)
    .filter(Number.isFinite);

  renderChart(state.history, range);
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

  const el = document.getElementById("currentTime");
  el.textContent = label;
  el.dateTime = now.toISOString();
}

function renderOfflineState() {
  if (USE_MOCK_DATA) return;

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
  setText("statusSource", USE_MOCK_DATA ? "Simulação" : "API REST");
}

async function refreshDashboard() {
  setBusy(true);
  setConnectionState("loading", "Carregando");
  setNotice("Atualizando leituras...", "loading", false);

  try {
    await Promise.all([loadLatest(), loadHistory(state.range)]);

    if (USE_MOCK_DATA) {
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

document.querySelectorAll(".range-btn").forEach(button => {
  button.addEventListener("click", async () => {
    document.querySelectorAll(".range-btn").forEach(item => item.classList.remove("active"));
    button.classList.add("active");
    state.range = button.dataset.range;

    setBusy(true);
    try {
      await loadHistory(state.range);
    } catch (error) {
      handleError(error);
    } finally {
      setBusy(false);
    }
  });
});

document.getElementById("retryButton").addEventListener("click", refreshDashboard);

window.addEventListener("offline", renderOfflineState);
window.addEventListener("online", () => {
  if (!USE_MOCK_DATA) refreshDashboard();
});

renderClock();
setInterval(renderClock, 1000);
refreshDashboard();
