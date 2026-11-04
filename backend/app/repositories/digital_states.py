"""Persistencia isolada dos estados digitais de chuva e luz."""
from functools import lru_cache

from psycopg import connect
from psycopg.rows import dict_row

from app.core.config import settings
from app.schemas.digital import DigitalState


class DigitalStateNotFound(LookupError):
    pass


class InMemoryDigitalStates:
    def __init__(self):
        self.data = {}

    def add(self, state: DigitalState):
        last = self.data.get(state.station_id)
        if last is None or state.timestamp >= last.timestamp:
            self.data[state.station_id] = state

    def latest(self, station_id: str) -> DigitalState:
        if station_id not in self.data:
            raise DigitalStateNotFound(station_id)
        return self.data[station_id]


class PostgresDigitalStates:
    def __init__(self, url: str):
        self.url = url

    def add(self, state: DigitalState):
        with connect(self.url, row_factory=dict_row) as conn, conn.cursor() as cur:
            cur.execute(
                """INSERT INTO stations (code,name) VALUES (%s,%s)
                ON CONFLICT(code) DO UPDATE SET updated_at=NOW()
                RETURNING id""",
                (state.station_id, state.station_id.replace("-", " ").title()),
            )
            station_db_id = cur.fetchone()["id"]
            cur.execute(
                """INSERT INTO station_digital_states
                (station_id,observed_at,rain_detected,dark)
                VALUES (%s,%s,%s,%s)""",
                (station_db_id, state.timestamp, state.rain_detected, state.dark),
            )

    def latest(self, station_id: str) -> DigitalState:
        with connect(self.url, row_factory=dict_row) as conn, conn.cursor() as cur:
            cur.execute(
                """SELECT s.code AS station_id,
                d.observed_at AS timestamp,d.rain_detected,d.dark
                FROM station_digital_states d
                JOIN stations s ON s.id=d.station_id
                WHERE s.code=%s ORDER BY d.observed_at DESC,d.id DESC LIMIT 1""",
                (station_id,),
            )
            row = cur.fetchone()
        if row is None:
            raise DigitalStateNotFound(station_id)
        return DigitalState.model_validate(row)


@lru_cache(maxsize=1)
def get_digital_states_repository():
    if settings.database_url:
        return PostgresDigitalStates(settings.database_url)
    return InMemoryDigitalStates()
