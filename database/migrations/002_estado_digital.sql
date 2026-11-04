-- Tabela independente para estados digitais experimentais.
-- Nao transforma deteccao de chuva em mm nem LDR digital em %.
CREATE TABLE IF NOT EXISTS station_digital_states (
  id BIGSERIAL PRIMARY KEY,
  station_id BIGINT NOT NULL REFERENCES stations(id) ON DELETE CASCADE,
  observed_at TIMESTAMPTZ NOT NULL,
  rain_detected BOOLEAN NOT NULL,
  dark BOOLEAN NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS digital_states_station_time_idx
  ON station_digital_states(station_id, observed_at DESC);
