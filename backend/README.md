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

Para permitir integração completa de software antes do MQTT, `POST /api/v1/telemetry` pode validar e persistir uma mensagem no repositório ativo. Esse endpoint é de apoio ao desenvolvimento, fica desabilitado por padrão e só responde quando `ENABLE_HTTP_INGESTION=true`. Ele não substitui MQTT como transporte principal.

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


## MQTT

O consumidor MQTT já está implementado como worker separado do servidor HTTP. Como processos separados não compartilham o repositório em memória, o worker exige `DATABASE_URL` para usar PostgreSQL como armazenamento compartilhado.

Configurações disponíveis:

```text
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883
MQTT_SUBSCRIPTION_TOPIC=estacao/+/telemetry
LOG_LEVEL=INFO
```

Execução:

```bash
PYTHONPATH=backend python -m app.workers.mqtt_consumer
```

No Windows PowerShell:

```powershell
$env:PYTHONPATH="backend"
python -m app.workers.mqtt_consumer
```

O worker valida:

- formato do tópico `estacao/<station_id>/telemetry`;
- JSON UTF-8;
- contrato de telemetria v1.0;
- correspondência entre o `station_id` do tópico e o payload.

Somente depois da validação a mensagem é enviada ao repositório ativo.

## Evidências sem hardware

Os testes automatizados validam:

```text
mensagem MQTT simulada
        ↓
validação de tópico e contrato
        ↓
repositório em memória
        ↓
serviço de consulta
        ↓
API REST
```

O CI também sobe uma instância PostgreSQL 16 temporária e executa um roundtrip real de persistência e consulta usando a migration do projeto.

Essas evidências validam integração de software e runtime do banco. Elas não representam comunicação com ESP32, broker MQTT real em campo ou sensores físicos.


## Integração ponta a ponta com broker real

O CI possui um ensaio dedicado que inicia um broker Mosquitto real e executa:

```text
publisher Paho sintético
→ Mosquitto
→ worker MQTT
→ PostgreSQL
→ FastAPI
→ API REST
```

O teste está em:

```text
backend/tests/integration/test_broker_e2e.py
```

A configuração mínima do broker de CI está em:

```text
backend/tests/integration/mosquitto-ci.conf
```

Esse ensaio valida transporte MQTT real entre processos de software. Ele não representa publicação pelo ESP32 nem validação física dos sensores.
