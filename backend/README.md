# Backend

Backend FastAPI da Estação Meteorológica Inteligente.

## Estado atual

A API REST de consulta usada pelo dashboard já funciona sem hardware por meio de um repositório em memória abastecido com dados sintéticos determinísticos.

Esse modo existe apenas para desenvolvimento e integração de software. Os valores não representam medições físicas.

Endpoints disponíveis:

```text
GET  /health
POST /api/v1/telemetry/validate
GET  /api/v1/stations
GET  /api/v1/stations/{station_id}/latest
GET  /api/v1/stations/{station_id}/measurements?range=24h|7d|30d
GET  /api/v1/stations/{station_id}/summary?range=24h|7d|30d
```

O dashboard também é servido pelo próprio FastAPI:

```text
GET /dashboard/
```

A raiz `/` redireciona para `/dashboard/`.

## Execução local

Na raiz do repositório:

```bash
python -m pip install -r backend/requirements.txt
PYTHONPATH=backend uvicorn app.main:app --reload
```

No Windows PowerShell:

```powershell
$env:PYTHONPATH="backend"
python -m uvicorn app.main:app --reload
```

Depois acesse:

```text
http://127.0.0.1:8000/
```

## Integração sem hardware

Enquanto a ingestão MQTT e a persistência PostgreSQL em runtime ainda não estão conectadas, o serviço usa `InMemoryMeasurementRepository` com histórico sintético criado em `app/core/demo_data.py`.

A organização separa API, serviço e repositório para permitir substituir essa implementação posteriormente sem alterar o contrato consumido pelo dashboard.

Fluxo atual de desenvolvimento:

```text
Dados sintéticos -> Repository -> Service -> FastAPI -> Dashboard
```

Fluxo alvo:

```text
MQTT -> Backend -> PostgreSQL -> Service -> API REST -> Dashboard
```

## Contrato

As respostas de leitura preservam o contrato de telemetria v1.0, incluindo:

- `schema_version`;
- `station_id`;
- `timestamp`;
- `location`;
- `measurements`;
- `quality`.

O backend não converte valor ausente em zero.

## Testes

```bash
PYTHONPATH=backend python -m pytest backend/tests -q
```

Os testes incluem contrato, validação, endpoints de consulta, períodos suportados, estação inexistente e entrega do dashboard pelo FastAPI.
