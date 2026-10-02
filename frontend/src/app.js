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

function formatDateTime(value) {
  return new Intl.DateTimeFormat("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  }).format(new Date(value));
}

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

function metricLabel(value, suffix = "") {
  if (value === null || value === undefined) return "--";
  return `${value}${suffix}`;
}

function renderLatest(payload) {
  state.latest = payload;
  const m = payload.measurements;

  setText("stationName", payload.station_id.replace("-", " ").replace(/\b\w/g, c => c.toUpperCase()));
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
  setText("statusStation", "Operacional");
  setText("statusData", "Parcialmente válido");
  setText("statusSource", USE_MOCK_DATA ? "Simulação" : "API REST");
  setText("statusUpdated", formatDateTime(payload.timestamp));

  const note = m.temperature_c >= 26 ? "Leitura acima da média do período" :
               m.temperature_c <= 20 ? "Leitura abaixo da média do período" :
               "Leitura dentro da faixa recente";
  setText("temperatureNote", note);

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

  const container = document.getElementById("qualityList");
  container.innerHTML = "";

  Object.entries(quality).forEach(([key, status]) => {
    const tag = document.createElement("span");
    tag.className = "quality-tag";
    tag.dataset.status = status;
    tag.textContent = `${labels[key]} · ${status}`;
    container.appendChild(tag);
  });
}

function renderChart(values, range) {
  const svg = document.getElementById("temperatureChart");
  const width = 760;
  const height = 280;
  const pad = { top: 20, right: 16, bottom: 32, left: 38 };

  const min = Math.min(...values);
  const max = Math.max(...values);
  const avg = values.reduce((sum, value) => sum + value, 0) / values.length;
  const spread = Math.max(max - min, 2);
  const yMin = min - spread * 0.25;
  const yMax = max + spread * 0.25;

  setText("chartMin", `${min.toFixed(1)}°`);
  setText("chartAvg", `${avg.toFixed(1)}°`);
  setText("chartMax", `${max.toFixed(1)}°`);

  const x = i => pad.left + (i / Math.max(values.length - 1, 1)) * (width - pad.left - pad.right);
  const y = value => pad.top + ((yMax - value) / (yMax - yMin)) * (height - pad.top - pad.bottom);

  const linePoints = values.map((value, i) => `${x(i)},${y(value)}`).join(" ");
  const areaPoints = `${pad.left},${height - pad.bottom} ${linePoints} ${width - pad.right},${height - pad.bottom}`;

  const yTicks = Array.from({ length: 4 }, (_, i) => yMin + ((yMax - yMin) / 3) * i);
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

  const xLabels = labels.map((label, i) => {
    const xx = pad.left + (i / (labels.length - 1)) * (width - pad.left - pad.right);
    return `<text class="chart-label" text-anchor="${i === 0 ? "start" : i === labels.length - 1 ? "end" : "middle"}" x="${xx}" y="${height - 6}">${label}</text>`;
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

  const response = await fetch(`${API_BASE}/api/v1/stations/${state.station}/latest`);
  if (!response.ok) throw new Error("Não foi possível carregar a leitura atual.");
  renderLatest(await response.json());
}

async function loadHistory(range) {
  if (USE_MOCK_DATA) {
    renderChart(historySets[range], range);
    return;
  }

  const response = await fetch(`${API_BASE}/api/v1/stations/${state.station}/measurements?range=${range}`);
  if (!response.ok) throw new Error("Não foi possível carregar o histórico.");
  const data = await response.json();
  renderChart(data.map(item => item.temperature_c).filter(Number.isFinite), range);
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

function handleError(error) {
  console.error(error);
  setText("connectionLabel", "Indisponível");
  setText("statusStation", "Sem conexão");
  setText("statusData", "Não disponível");
  setText("statusSource", "API REST");
}

document.querySelectorAll(".range-btn").forEach(button => {
  button.addEventListener("click", async () => {
    document.querySelectorAll(".range-btn").forEach(item => item.classList.remove("active"));
    button.classList.add("active");
    state.range = button.dataset.range;

    try {
      await loadHistory(state.range);
    } catch (error) {
      handleError(error);
    }
  });
});

renderClock();
setInterval(renderClock, 1000);

Promise.all([loadLatest(), loadHistory(state.range)]).catch(handleError);
