import { metricConfig } from "./config.js";

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) element.textContent = value;
}

function formatMetric(value, metric) {
  if (!Number.isFinite(value)) return "--";
  const config = metricConfig[metric];
  return `${value.toFixed(config.decimals)} ${config.unit}`;
}

function xAxisLabels(range) {
  if (range === "24h") return ["00h", "06h", "12h", "18h", "Agora"];
  if (range === "7d") return ["7d", "5d", "3d", "1d", "Hoje"];
  return ["30d", "21d", "14d", "7d", "Hoje"];
}

function showChartEmpty(show) {
  document.getElementById("chartEmpty").hidden = !show;
  document.getElementById("historyChart").hidden = show;
}

export function renderChart(values, range, metric) {
  const cleanValues = values.filter(Number.isFinite);
  const config = metricConfig[metric];
  setText("historyTitle", config.label);
  setText("chartDescription", `Histórico de ${config.label.toLowerCase()} no período de ${range}.`);

  if (cleanValues.length < 2) {
    showChartEmpty(true);
    ["chartMin", "chartAvg", "chartMax"].forEach(id => setText(id, "--"));
    return;
  }

  showChartEmpty(false);
  const svg = document.getElementById("historyChart");
  const width = 760, height = 280;
  const pad = { top: 20, right: 16, bottom: 32, left: 48 };
  const min = Math.min(...cleanValues), max = Math.max(...cleanValues);
  const avg = cleanValues.reduce((sum, value) => sum + value, 0) / cleanValues.length;
  const spread = Math.max(max - min, metric === "pressure_hpa" ? 4 : 2);
  const yMin = min - spread * 0.25, yMax = max + spread * 0.25;
  setText("chartMin", formatMetric(min, metric));
  setText("chartAvg", formatMetric(avg, metric));
  setText("chartMax", formatMetric(max, metric));

  const x = index => pad.left + (index / Math.max(cleanValues.length - 1, 1)) * (width - pad.left - pad.right);
  const y = value => pad.top + ((yMax - value) / (yMax - yMin)) * (height - pad.top - pad.bottom);
  const linePoints = cleanValues.map((value, index) => `${x(index)},${y(value)}`).join(" ");
  const areaPoints = `${pad.left},${height - pad.bottom} ${linePoints} ${width - pad.right},${height - pad.bottom}`;
  const yTicks = Array.from({ length: 4 }, (_, index) => yMin + ((yMax - yMin) / 3) * index);
  const grid = yTicks.map(tick => {
    const yy = y(tick);
    const label = metric === "pressure_hpa" ? tick.toFixed(0) : tick.toFixed(config.decimals);
    return `<line class="chart-grid" x1="${pad.left}" x2="${width-pad.right}" y1="${yy}" y2="${yy}" /><text class="chart-label" x="0" y="${yy+4}">${label}</text>`;
  }).join("");
  const labels = xAxisLabels(range);
  const labelsSvg = labels.map((label,index) => {
    const xx=pad.left+(index/(labels.length-1))*(width-pad.left-pad.right);
    const anchor=index===0?"start":index===labels.length-1?"end":"middle";
    return `<text class="chart-label" text-anchor="${anchor}" x="${xx}" y="${height-6}">${label}</text>`;
  }).join("");
  svg.innerHTML = `${grid}<polygon class="chart-area" points="${areaPoints}" /><polyline class="chart-line" points="${linePoints}" />${labelsSvg}`;
}
