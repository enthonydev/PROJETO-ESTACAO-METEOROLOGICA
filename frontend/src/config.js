export const API_BASE = "";
export const USE_MOCK_DATA = window.location.protocol === "file:";
export const AUTO_REFRESH_MS = 60_000;

export const metricConfig = {
  temperature_c: { label: "Temperatura", unit: "°C", decimals: 1 },
  humidity_pct: { label: "Umidade", unit: "%", decimals: 0 },
  pressure_hpa: { label: "Pressão", unit: "hPa", decimals: 0 },
  air_quality_raw: { label: "Qualidade do ar", unit: "raw", decimals: 0 },
  luminosity_pct: { label: "Luminosidade", unit: "% relativa", decimals: 0 }
};

export const requiredMeasurementKeys = [
  "temperature_c",
  "humidity_pct",
  "pressure_hpa",
  "air_quality_raw",
  "luminosity_pct",
  "rain_mm"
];
