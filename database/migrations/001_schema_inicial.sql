-- Schema inicial compatível com o contrato de telemetria v1.0.
-- Faixas físicas e calibrações permanecem pendentes de validação.

CREATE TABLE stations (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE measurements (
    id BIGSERIAL PRIMARY KEY,
    station_id BIGINT NOT NULL REFERENCES stations (id),
    measured_at TIMESTAMPTZ NOT NULL,
    temperature_c DOUBLE PRECISION,
    humidity_pct DOUBLE PRECISION,
    pressure_hpa DOUBLE PRECISION,
    air_quality_raw DOUBLE PRECISION,
    luminosity_pct DOUBLE PRECISION,
    rain_mm DOUBLE PRECISION,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE measurement_quality (
    id BIGSERIAL PRIMARY KEY,
    measurement_id BIGINT NOT NULL REFERENCES measurements (id) ON DELETE CASCADE,
    metric VARCHAR(50) NOT NULL,
    status VARCHAR(16) NOT NULL,
    reason TEXT,
    CONSTRAINT measurement_quality_metric_ck CHECK (
        metric IN ('temperature', 'humidity', 'pressure', 'air_quality', 'luminosity', 'rain')
    ),
    CONSTRAINT measurement_quality_status_ck CHECK (
        status IN ('ok', 'suspect', 'invalid', 'error')
    ),
    CONSTRAINT measurement_quality_metric_uk UNIQUE (measurement_id, metric)
);

CREATE INDEX measurements_station_measured_at_idx
    ON measurements (station_id, measured_at);
