import { API_BASE, requiredMeasurementKeys } from "./config.js";

export function validateTelemetry(payload) {
  if (!payload || typeof payload !== "object") throw new Error("Resposta de telemetria ausente.");
  if (payload.schema_version !== "1.0") throw new Error("Versão de telemetria incompatível.");
  if (!payload.station_id || typeof payload.station_id !== "string") throw new Error("Identificação da estação ausente.");
  if (!payload.measurements || !payload.quality) throw new Error("Telemetria incompleta.");
  const missingKey = requiredMeasurementKeys.find(key => !(key in payload.measurements));
  if (missingKey) throw new Error(`Métrica ausente no payload: ${missingKey}`);
  return payload;
}

async function fetchJson(url, failureLabel) {
  const response = await fetch(url, { headers: { Accept: "application/json" } });
  if (!response.ok) throw new Error(`${failureLabel} (HTTP ${response.status}).`);
  return response.json();
}

export function fetchLatest(station) {
  return fetchJson(`${API_BASE}/api/v1/stations/${station}/latest`, "Falha ao carregar leitura atual");
}

export function fetchHistory(station, range) {
  return fetchJson(
    `${API_BASE}/api/v1/stations/${station}/measurements?range=${encodeURIComponent(range)}`,
    "Falha ao carregar histórico"
  );
}
