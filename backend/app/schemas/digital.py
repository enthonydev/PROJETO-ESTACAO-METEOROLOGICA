"""Estado digital experimental independente do contrato de telemetria v1.0."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class DigitalState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    station_id: str = Field(min_length=1, max_length=100)
    timestamp: datetime
    rain_detected: bool
    dark: bool

    @field_validator("rain_detected", "dark", mode="before")
    @classmethod
    def require_bool(cls, value):
        if type(value) is not bool:
            raise ValueError("estado digital deve ser booleano")
        return value

    @field_validator("timestamp")
    @classmethod
    def require_timezone(cls, value):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("timestamp deve incluir fuso")
        return value
