const baseMockLatest = {
  schema_version: "1.0",
  station_id: "estacao-01",
  timestamp: new Date().toISOString(),
  location: { latitude: null, longitude: null },
  measurements: {
    temperature_c: 24.8, humidity_pct: 63, pressure_hpa: 1012,
    air_quality_raw: 184, luminosity_pct: 72, rain_mm: null
  },
  quality: {
    temperature: "ok", humidity: "ok", pressure: "ok",
    air_quality: "suspect", luminosity: "ok", rain: "error"
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

export function buildMockLatest(demoMode) {
  const payload = structuredClone(baseMockLatest);
  payload.timestamp = new Date().toISOString();
  if (demoMode === "partial") {
    payload.measurements.air_quality_raw = null;
    payload.quality.air_quality = "error";
  }
  if (demoMode === "invalid") payload.schema_version = "2.0";
  return payload;
}

export function getMockHistory(range, metric, demoMode) {
  if (demoMode === "empty") return [];
  return mockHistory[range]?.[metric] ?? [];
}
