const API_BASE = "";
const USE_MOCK_DATA = true;
const AUTO_REFRESH_MS = 60_000;

const metricConfig = {
  temperature_c: { label: "Temperatura", unit: "°C", decimals: 1 },
  humidity_pct: { label: "Umidade", unit: "%", decimals: 0 },
  pressure_hpa: { label: "Pressão", unit: "hPa", decimals: 0 },
  air_quality_raw: { label: "Qualidade do ar", unit: "raw", decimals: 0 },
  luminosity_pct: { label: "Luminosidade", unit: "% relativa", decimals: 0 }
};

const state = {
  range: "24h",
  metric: "temperature_c",
  station: "estacao-01",
  latest: null,
  history: [],
  lastSuccessfulRefresh: null
};

const baseMockLatest = {
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

const mockHistory = {
  "24h": {
    temperature_c: [22.8,22.4,22.1,21.9,21.8,22.2,23.1,24.4,25.6,26.4,27.1,27.5,27.2,26.8,26.3,25.9,25.5,25.2,24.9,24.7,24.5,24.4,24.6,24.8],
    humidity_pct: [71,73,74,75,76,74,71,68,64,60,57,55,54,55,57,59,61,62,63,64,65,65,64,63],
    pressure_hpa: [1014,1014,1014,1013,1013,1013,1013,1012,1012,1012,1011,1011,1011,1011,1012,1012,1012,1012,1012,1013,1013,1013,1012,1012],
    air_quality_raw: [168,170,171,169,166,165,170,176,180,184,190,194,197,192,188,185,182,180,179,181,183,185,184,184],
    luminosity_pct: [2,1,1,1,2,8,20,38,56,69,78,84,87,83,77,68,55,41,28,17,9,5,3,2]
  },
  "7d": {
    temperature_c: [23.6,24.1,23.9,25.0,24.5,24.7,24.8],
    humidity_pct: [67,65,69,61,64,63,63],
    pressure_hpa: [1013,1011,1014,1012,1010,1013,1012],
    air_quality_raw: [178,181,176,190,187,182,184],
    luminosity_pct: [66,71,62,75,68,70,72]
  },
  "30d": {
    temperature_c: [23.1,23.4,23.8,24.0,24.3,24.2,24.5,24.8,25.1,24.7,24.5,24.9,25.2,25.4,25.0,24.6,24.3,24.1,24.4,24.8,25.1,25.3,25.0,24.7,24.5,24.4,24.6,24.7,24.8,24.8],
    humidity_pct: [70,69,68,67,65,64,63,62,61,63,64,62,60,59,61,63,65,66,64,62,60,59,61,63,65,64,63,62,63,63],
    pressure_hpa: [1014,1013,1014,1012,1013,1012,1011,1012,1011,1010,1011,1012,1012,1011,1012,1013,1014,1013,1012,1011,1010,1011,1012,1013,1012,1012,1013,1013,1012,1012],
    air_quality_raw: [169,172,175,174,178,180,183,185,188,186,184,182,179,181,185,189,191,187,183,180,178,181,184,186,188,187,185,183,184,184],
    luminosity_pct: [62,64,67,65,69,70,72,74,76,71,68,73,75,78,74,70,66,64,67,71,73,76,72,69,68,70,71,73,72,72]
  }
};

const requiredMeasurementKeys = [
  "temperature_c",
  "humidity_pct",
  "pressure_hpa",
  "air_quality_raw",
  "luminosity_pct",
  "rain_mm"
];

const demoMode = new URLSearchParams(window.location.search).get("demo");

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

function formatMetric(value, metric) {
  if (!Number.isFinite(value)) return "--";
  const config = metricConfig[metric];
  return `${value.toFixed(config.decimals)} ${config.unit}`;
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

function validateTelemetry(payload) {
  if (!payload || typeof payload !== "object") throw new Error("Resposta de telemetria ausente.");
  if (payload.schema_version !== "1.0") throw new Error("Versão de telemetria incompatível.");
  if (!payload.station_id || typeof payload.station_id !== "string") throw new Error("Identificação da estação ausente.");
  if (!payload.measurements || !payload.quality) throw new Error("Telemetria incompleta.");

  const missingKey = requiredMeasurementKeys.find(key => !(key in payload.measurements));
  if (missingKey) throw new Error(`Métrica ausente no payload: ${missingKey}`);

  return payload;
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
  setText("statusStation", USE_MOCK_DATA ? "Demonstração" : "Operacional");
  setText("statusData", deriveDataState(payload.quality));
  setText("statusSource", USE_MOCK_DATA ? "Simulação" : "API REST");
  setText("statusUpdated", formatDateTime(payload.timestamp));
  setText("statusSchema", payload.schema_version);
  setText(
    "temperatureNote",
    USE_MOCK_DATA ? "Leitura simulada para desenvolvimento da interface" : "Leitura recebida da estação"
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

function showChartEmpty(show) {
  document.getElementById("chartEmpty").hidden = !show;
  document.getElementById("historyChart").hidden = show;
}

function xAxisLabels(range) {
  if (range === "24h") return ["00h", "06h", "12h", "18h", "Agora"];
  if (range === "7d") return ["7d", "5d", "3d", "1d", "Hoje"];
  return ["30d", "21d", "14d", "7d", "Hoje"];
}

function renderChart(values, range, metric) {
  const cleanValues = values.filter(Number.isFinite);
  const config = metricConfig[metric];

  setText("historyTitle", config.label);
  setText("chartDescription", `Histórico de ${config.label.toLowerCase()} no período de ${range}.`);

  if (cleanValues.length < 2) {
    showChartEmpty(true);
    setText("chartMin", "--");
    setText("chartAvg", "--");
    setText("chartMax", "--");
    return;
  }

  showChartEmpty(false);

  const svg = document.getElementById("historyChart");
  const width = 760;
  const height = 280;
  const pad = { top: 20, right: 16, bottom: 32, left: 48 };

  const min = Math.min(...cleanValues);
  const max = Math.max(...cleanValues);
  const avg = cleanValues.reduce((sum, value) => sum + value, 0) / cleanValues.length;
  const spread = Math.max(max - min, metric === "pressure_hpa" ? 4 : 2);
  const yMin = min - spread * 0.25;
  const yMax = max + spread * 0.25;

  setText("chartMin", formatMetric(min, metric));
  setText("chartAvg", formatMetric(avg, metric));
  setText("chartMax", formatMetric(max, metric));

  const x = index => pad.left + (index / Math.max(cleanValues.length - 1, 1)) * (width - pad.left - pad.right);
  const y = value => pad.top + ((yMax - value) / (yMax - yMin)) * (height - pad.top - pad.bottom);

  const linePoints = cleanValues.map((value, index) => `${x(index)},${y(value)}`).join(" ");
  const areaPoints = `${pad.left},${height - pad.bottom} ${linePoints} ${width - pad.right},${height - pad.bottom}`;

  const yTicks = Array.from({ length: 4 }, (_, index) => yMin + ((yMax - yMin) / 3) * index);
  const labels = xAxisLabels(range);

  const grid = yTicks.map(tick => {
    const yy = y(tick);
    const tickLabel = metric === "pressure_hpa" ? tick.toFixed(0) : tick.toFixed(config.decimals);
    return `
      <line class="chart-grid" x1="${pad.left}" x2="${width - pad.right}" y1="${yy}" y2="${yy}" />
      <text class="chart-label" x="0" y="${yy + 4}">${tickLabel}</text>
    `;
  }).join("");

  const labelsSvg = labels.map((label, index) => {
    const xx = pad.left + (index / (labels.length - 1)) * (width - pad.left - pad.right);
    const anchor = index === 0 ? "start" : index === labels.length - 1 ? "end" : "middle";
    return `<text class="chart-label" text-anchor="${anchor}" x="${xx}" y="${height - 6}">${label}</text>`;
  }).join("");

  svg.innerHTML = `
    ${grid}
    <polygon class="chart-area" points="${areaPoints}" />
    <polyline class="chart-line" points="${linePoints}" />
    ${labelsSvg}
  `;
}

function buildMockLatest() {
  const payload = structuredClone(baseMockLatest);
  payload.timestamp = new Date().toISOString();

  if (demoMode === "partial") {
    payload.measurements.air_quality_raw = null;
    payload.quality.air_quality = "error";
  }

  if (demoMode === "invalid") {
    payload.schema_version = "2.0";
  }

  return payload;
}

function getMockHistory(range, metric) {
  if (demoMode === "empty") return [];
  return mockHistory[range]?.[metric] ?? [];
}

async function loadLatest() {
  if (demoMode === "error") throw new Error("Falha simulada da API para teste da interface.");

  if (USE_MOCK_DATA) {
    renderLatest(buildMockLatest());
    return;
  }

  const response = await fetch(`${API_BASE}/api/v1/stations/${state.station}/latest`, {
    headers: { Accept: "application/json" }
  });

  if (!response.ok) throw new Error(`Falha ao carregar leitura atual (HTTP ${response.status}).`);
  renderLatest(await response.json());
}

async function loadHistory(range, metric) {
  if (demoMode === "error") throw new Error("Falha simulada da API para teste da interface.");

  if (USE_MOCK_DATA) {
    state.history = getMockHistory(range, metric);
    renderChart(state.history, range, metric);
    return;
  }

  const response = await fetch(
    `${API_BASE}/api/v1/stations/${state.station}/measurements?range=${encodeURIComponent(range)}`,
    { headers: { Accept: "application/json" } }
  );

  if (!response.ok) throw new Error(`Falha ao carregar histórico (HTTP ${response.status}).`);

  const data = await response.json();
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
    await Promise.all([
      loadLatest(),
      loadHistory(state.range, state.metric)
    ]);

    state.lastSuccessfulRefresh = new Date();

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
  if (!USE_MOCK_DATA) refreshDashboard();
});

renderClock();
setInterval(renderClock, 1000);
setInterval(() => {
  if (!document.hidden) refreshDashboard();
}, AUTO_REFRESH_MS);

refreshDashboard();
