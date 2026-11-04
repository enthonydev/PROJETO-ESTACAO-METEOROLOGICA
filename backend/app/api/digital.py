"""Leituras digitais, em rota separada para preservar contrato v1.0."""
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.repositories.digital_states import (
    DigitalStateNotFound,
    get_digital_states_repository,
)
from app.schemas.digital import DigitalState

router = APIRouter(tags=["digital"])


@router.get("/api/v1/stations/{station_id}/digital/latest", response_model=DigitalState)
def digital_latest(station_id: str, repository=Depends(get_digital_states_repository)):
    try:
        return repository.latest(station_id)
    except DigitalStateNotFound as exc:
        raise HTTPException(status_code=404, detail="Sem estado digital para esta estação") from exc


@router.post("/api/v1/digital", response_model=DigitalState, status_code=status.HTTP_201_CREATED)
def ingest_digital(payload: DigitalState, repository=Depends(get_digital_states_repository)):
    # Apenas ponte USB local em ambiente de desenvolvimento.
    if not settings.enable_http_ingestion:
        raise HTTPException(status_code=404, detail="Ingestao HTTP desabilitada")
    repository.add(payload)
    return payload
