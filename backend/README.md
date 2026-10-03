# Backend

Backend FastAPI da Estação Meteorológica Inteligente.

## Estado atual

A API REST de consulta usada pelo dashboard já funciona sem hardware por meio de um repositório em memória abastecido com dados sintéticos determinísticos.

Esse modo existe apenas para desenvolvimento e integração de software. Os valores não representam medições físicas.

Endpoints disponíveis:

```text
GET  /health
POST /api/v1/telemetry/validate
POST /api/v1/telemetry
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

Sem `DATABASE_URL`, o serviço usa `InMemoryMeasurementRepository` com histórico sintético criado em `app/core/demo_data.py`. Quando `DATABASE_URL` é configurada, a mesma camada de serviço passa a usar `PostgresMeasurementRepository`, compatível com `database/migrations/001_schema_inicial.sql`.

A organização separa API, serviço e repositório para permitir substituir essa implementação posteriormente sem alterar o contrato consumido pelo dashboard.

Para permitir integração completa de software antes do MQTT, `POST /api/v1/telemetry` valida e persiste uma mensagem no repositório ativo. Esse endpoint é de apoio ao desenvolvimento e não substitui MQTT como transporte principal.

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


## PostgreSQL

Para usar persistência real sem hardware:

1. crie um banco PostgreSQL;
2. aplique `database/migrations/001_schema_inicial.sql`;
3. defina `DATABASE_URL`;
4. inicie o FastAPI normalmente.

Exemplo de formato da variável, sem credenciais reais:

```text
postgresql://usuario:senha@localhost:5432/estacao
```

Com o banco ativo, é possível enviar payloads de teste por `POST /api/v1/telemetry` e consultá-los imediatamente pelo dashboard.
