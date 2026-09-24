# Arquitetura do Projeto — Estação Meteorológica Inteligente

## 1. Objetivo

Este documento define a baseline arquitetural do projeto acadêmico de estação meteorológica inteligente. A solução integra ESP32, sensores ambientais, interfaces OLED locais, conectividade Wi-Fi, telemetria MQTT, backend Python, banco de dados relacional e dashboard web público.

Mudanças que alterem contratos, tecnologias centrais, persistência, fluxo de dados ou responsabilidades entre módulos devem ser registradas por ADR antes da implementação.

## 2. Visão geral

```text
                         ┌──────────────────────┐
                         │ API meteorológica    │
                         └──────────┬───────────┘
                                    │ HTTPS
                                    ▼
┌───────────────┐          ┌──────────────────────┐
│ Sensores      │─────────▶│ ESP32 / MicroPython  │
│ ambientais    │          │                      │
└───────────────┘          │ aquisição/validação  │
                           │ conectividade         │
┌───────────────┐          │ serviços de tempo    │
│ DS3231        │─────────▶│ renderização local   │
└───────────────┘          └─────┬─────────┬──────┘
                                  │         │
                            I2C   │         │ Wi-Fi / MQTT
                                  ▼         ▼
                           ┌──────────┐  ┌───────────┐
                           │TCA9548A  │  │  Broker   │
                           └──┬────┬──┘  └─────┬─────┘
                              │    │           │
                         CH0  │    │ CH1       ▼
                              ▼    ▼     ┌──────────────┐
                         OLED 1  OLED 2  │Backend Python│
                         Meteo   Relógio │   FastAPI    │
                                        └──────┬───────┘
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │ PostgreSQL   │
                                        └──────┬───────┘
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │ API REST v1  │
                                        └──────┬───────┘
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │ Dashboard Web│
                                        └──────────────┘
```

O dashboard web exigido academicamente e os dois displays locais são interfaces distintas. A API meteorológica externa complementa a interface embarcada e não substitui os sensores físicos responsáveis pelas medições da estação.

## 3. Hardware

### 3.1 Núcleo

- ESP32 DevKit V1.
- Firmware em MicroPython.
- Wi-Fi nativo.

### 3.2 Sensores ambientais

O escopo acadêmico prevê temperatura, umidade, pressão atmosférica, qualidade do ar, luminosidade e pluviometria. A baseline contempla DHT22, BMP280, MQ-135, LDR e pluviômetro conforme o plano de ensino.

O BME280 integra adicionalmente o subsistema local de visualização e fornece temperatura, umidade e pressão para a interface embarcada. A coexistência/necessidade final de sensores com funções sobrepostas deve ser validada fisicamente e documentada antes de qualquer simplificação do escopo exigido pelo professor.

### 3.3 Sistema de telas

Dois OLEDs independentes de 1,3", 128×64, SH1106, I2C:

- canal 0 do TCA9548A: OLED meteorológico;
- canal 1 do TCA9548A: OLED relógio/calendário.

O TCA9548A resolve possível colisão de endereço I2C entre displays iguais.

O display meteorológico apresenta estado já processado, combinando dados externos da API meteorológica e medições locais do BME280.

O display de relógio apresenta hora, minutos, data e dia da semana. NTP fornece correção periódica quando há internet e o DS3231 mantém referência local durante indisponibilidade de rede.

## 4. Arquitetura do firmware

Estrutura alvo:

```text
firmware/
├── src/
│   ├── main.py
│   ├── config/
│   ├── drivers/
│   │   ├── tca9548a.py
│   │   ├── sh1106.py
│   │   ├── bme280.py
│   │   └── ds3231.py
│   ├── services/
│   │   ├── weather_api.py
│   │   ├── time_service.py
│   │   ├── sensor_service.py
│   │   └── connectivity.py
│   ├── displays/
│   │   ├── weather_display.py
│   │   └── clock_display.py
│   ├── tasks/
│   │   ├── weather_task.py
│   │   ├── clock_task.py
│   │   ├── sensor_task.py
│   │   └── sync_task.py
│   └── models/
└── tests/
```

Drivers tratam hardware. Services obtêm e processam dados. Displays somente renderizam estado recebido. Tasks controlam periodicidade. Models representam estado e contratos internos.

Nenhuma tela deve consultar diretamente API, NTP ou sensores.

### 4.1 Periodicidades

Devem existir ciclos independentes para:

- atualização do relógio;
- leitura do BME280;
- aquisição dos demais sensores;
- renderização meteorológica;
- consulta à API meteorológica;
- sincronização NTP/RTC;
- renderização de data/hora;
- publicação MQTT.

Não utilizar um único ciclo bloqueante para todas as funcionalidades. Rotinas cooperativas, como `uasyncio`, são a preferência arquitetural, condicionada à validação de estabilidade no ESP32 real.

### 4.2 Operação degradada

- queda de Wi-Fi não congela displays nem aquisição local;
- falha da API mantém o último dado externo válido;
- sensores locais continuam atualizando quando possível;
- ausência de internet não interrompe relógio por causa do DS3231;
- retorno do NTP corrige a referência temporal de maneira controlada;
- falha de um display não deve derrubar telemetria ou o outro display.

## 5. Telemetria

Fluxo principal:

```text
Sensores → ESP32 → Wi-Fi → MQTT → Backend → PostgreSQL
```

Tópico baseline:

```text
estacao/<station_id>/telemetry
```

Payload baseline:

```json
{
  "schema_version": "1.0",
  "station_id": "estacao-01",
  "timestamp": "ISO-8601",
  "location": {
    "latitude": null,
    "longitude": null
  },
  "measurements": {
    "temperature_c": 0.0,
    "humidity_pct": 0.0,
    "pressure_hpa": 0.0,
    "air_quality_raw": 0,
    "luminosity_pct": 0.0,
    "rain_mm": 0.0
  },
  "quality": {
    "temperature": "ok",
    "humidity": "ok",
    "pressure": "ok",
    "air_quality": "ok",
    "luminosity": "ok",
    "rain": "ok"
  }
}
```

O schema é versionado. Mudança incompatível exige decisão arquitetural e estratégia de compatibilidade.

## 6. Backend

Baseline: Python + FastAPI.

Responsabilidades:

- consumir telemetria;
- validar schema e integridade;
- aplicar regras de negócio;
- persistir dados;
- fornecer consultas e agregações;
- expor API REST ao dashboard;
- registrar falhas de ingestão.

Separação alvo:

```text
backend/app/
├── api/
├── core/
├── models/
├── schemas/
├── services/
└── repositories/
```

Endpoints baseline:

- `GET /health`
- `GET /api/v1/stations`
- `GET /api/v1/stations/{id}/latest`
- `GET /api/v1/stations/{id}/measurements`
- `GET /api/v1/stations/{id}/summary`

## 7. Persistência

Baseline: PostgreSQL.

Entidades iniciais:

### stations

Identidade, código, nome, latitude, longitude, estado ativo e timestamps.

### measurements

Estação, instante medido, temperatura, umidade, pressão, qualidade do ar, luminosidade, chuva e timestamps.

### measurement_quality

Medição, métrica, estado de qualidade e motivo.

Índice principal de série temporal: `station_id + measured_at`.

Política temporal recomendada: armazenar UTC e converter na apresentação.

SQLite pode ser utilizado em desenvolvimento/testes quando não alterar a semântica do modelo.

## 8. Dashboard

O dashboard é público, responsivo e desacoplado do banco.

Fluxo:

```text
Dashboard → API REST → Backend → PostgreSQL
```

Deve conter, conforme disponibilidade:

- cards de métricas atuais;
- gráficos históricos;
- seleção de período;
- localização da estação em mapa;
- estados de carregamento, erro e ausência de dados;
- requisitos básicos de acessibilidade.

Chart.js e Leaflet/OpenStreetMap são opções baseline, não obrigações imutáveis.

## 9. Validação

A validação ocorre no firmware e novamente no backend.

Princípios:

- não inventar valor quando a leitura falhar;
- marcar qualidade da métrica;
- rejeitar timestamp ou schema inválido;
- não associar silenciosamente estação desconhecida;
- não declarar unidade/conversão não sustentada por datasheet ou calibração;
- MQ-135 permanece como indicador/raw até existir calibração tecnicamente defensável.

## 10. Estrutura alvo do repositório

```text
.github/
docs/
├── arquitetura/
│   └── adr/
├── requisitos/
├── testes/
├── academico/
└── evidencias/
firmware/
hardware/
├── diagrams/
├── wokwi/
├── datasheets/
├── pinout.md
└── bom.md
backend/
frontend/
database/
├── migrations/
├── schema/
├── seeds/
└── diagrams/
scripts/
README.md
CONTRIBUTING.md
```

A estrutura deve ser criada incrementalmente; diretórios vazios não precisam existir antes de terem conteúdo real.

## 11. Segurança e configuração

- segredos, SSID, senhas, tokens e credenciais não são versionados;
- usar arquivos de exemplo para configuração;
- dashboard não acessa banco diretamente;
- entradas externas são validadas;
- CORS deve ser explícito;
- logs não podem expor segredos.

## 12. Testes

Camadas mínimas:

1. drivers e funções de validação do firmware;
2. sensores individualmente;
3. serialização e contrato de telemetria;
4. ingestão/backend;
5. persistência;
6. API;
7. frontend;
8. integração ponta a ponta;
9. operação offline/recuperação;
10. testes de campo.

Evidência simulada e física devem ser identificadas separadamente.

## 13. Governança arquitetural

Alterações relevantes exigem ADR em `docs/arquitetura/adr/`.

Um ADR deve registrar contexto, opções, decisão proposta, consequências, impacto e validação.

Nenhuma mudança arquitetural deve ser implementada enquanto estiver apenas proposta.

## 14. Governança Git

- `main` representa integração estável.
- Desenvolvimento ocorre em branches `feature/`, `fix/`, `docs/`, `chore/`, `test/` ou `refactor/`.
- Não fazer push direto na `main`.
- Todo trabalho segue para PR e revisão de PO.
- Commits devem possuir título e descrição em português.
- Antes do primeiro commit em um ambiente, confirmar `user.name` e `user.email` do integrante responsável.
- Não utilizar nomes de ferramentas/agentes em branches, arquivos ou documentação.
- Merge somente após revisão, testes e checks aplicáveis.

## 15. Decisões ainda não congeladas

Permanecem pendentes até validação:

- pinagem definitiva;
- modelo/fator do pluviômetro;
- calibração e interpretação final do MQ-135;
- infraestrutura final de hospedagem e broker;
- coordenadas físicas da estação;
- intervalos numéricos definitivos de validação;
- periodicidades exatas de cada task;
- eventual simplificação de sensores com funções sobrepostas.

Esses pontos devem permanecer explícitos como pendências. Não devem ser resolvidos por suposição.
