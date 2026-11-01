export const state = {
  range: "24h",
  metric: "temperature_c",
  station: new URLSearchParams(window.location.search).get("station") || "estacao-01",
  latest: null,
  history: [],
  lastSuccessfulRefresh: null
};
