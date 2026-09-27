# Arquitetura do Projeto — Estação Meteorológica Inteligente

## 1. Objetivo

Esta é a baseline arquitetural após o ADR-002. A estação mede localmente grandezas ambientais com ESP32 e sensores físicos, publica telemetria via Wi-Fi/MQTT, persiste dados no backend e disponibiliza API REST e dashboard. Uma única OLED fornece interface embarcada. API meteorológica externa e NTP são serviços complementares de rede.

Mudanças incompatíveis de contrato, tecnologia central, persistência ou responsabilidade entre módulos exigem ADR.

## 2. Visão geral

```text
DHT22 ─────────┐
BMP280 ────────┤
MQ-135 ────────┤
LDR ───────────┼──> ESP32 / MicroPython ── Wi-Fi ── MQTT ──> Backend/FastAPI
Sensor chuva ──┘            │                                  │
                            ├── I²C ──> OLED 128x64             ▼
                            ├── NTP                         PostgreSQL
                            └── API meteorológica               │
                                (complementar)                   ▼
                                                           API REST v1
                                                                │
                                                                ▼
                                                           Dashboard Web
```

A API meteorológica não substitui sensores físicos.

## 3. Hardware

### 3.1 Núcleo
- ESP32 DevKit V1;
- MicroPython;
- Wi-Fi nativo.

### 3.2 Sensores
- DHT22: temperatura e umidade;
- BMP280: pressão atmosférica;
- MQ-135: indicador bruto de qualidade do ar;
- LDR: luminosidade relativa;
- módulo de chuva: detecção/avaliação experimental.

Não declarar ppm, lux ou precipitação em mm sem calibração/método defensável.

### 3.3 Interface local
Uma OLED I²C 128x64 apresenta estado local, data/hora e, quando disponível, informação externa complementar. Não há TCA9548A nem segunda tela na baseline.

### 3.4 Tempo
NTP é a fonte de sincronização principal. Sem internet e sem RTC dedicado, o sistema pode manter apenas a referência disponível no relógio do runtime enquanto permanecer energizado. Essa limitação deve ser registrada nos testes.

## 4. Firmware

Estrutura lógica:

```text
drivers -> services -> models -> tasks -> interface local
                     |
                     +-> telemetria/MQTT
```

Drivers isolam hardware; services tratam aquisição e fontes externas; models representam estado; tasks controlam ciclos; a OLED apenas renderiza estado recebido.

Ciclos independentes:
- aquisição dos sensores;
- sincronização NTP;
- consulta opcional à API meteorológica;
- atualização da OLED;
- publicação MQTT.

A preferência é por execução cooperativa sem um ciclo único bloqueante.

### 4.1 Operação degradada
- falha de Wi-Fi não deve impedir aquisição local;
- falha da API externa não invalida sensores físicos;
- falha da OLED não derruba aquisição/telemetria;
- ausência de NTP deve ser sinalizada sem inventar timestamp confiável;
- falha de um sensor afeta sua métrica, não as demais.

## 5. Telemetria

Fluxo principal:

```text
Sensores -> ESP32 -> Wi-Fi -> MQTT -> Backend -> PostgreSQL
```

Tópico baseline: `estacao/<station_id>/telemetry`.

O schema v1.0 permanece vigente durante a transição. Campos: `temperature_c`, `humidity_pct`, `pressure_hpa`, `air_quality_raw`, `luminosity_pct` e `rain_mm`, acompanhados por qualidade.

### 5.1 Regra transitória de chuva
O módulo de chuva atual não é pluviômetro calibrado. Portanto `rain_mm` não pode receber milímetros inferidos arbitrariamente. Até existir método/fator validado, a métrica deve ser ausente/inválida conforme o contrato e a leitura experimental pode permanecer apenas no domínio interno/evidência de teste.

## 6. Backend e persistência

Baseline preservada: Python/FastAPI, PostgreSQL e API REST v1. O backend valida schema, persiste medições, fornece consultas/agregações e registra falhas.

Endpoints baseline:
- `GET /health`
- `GET /api/v1/stations`
- `GET /api/v1/stations/{id}/latest`
- `GET /api/v1/stations/{id}/measurements`
- `GET /api/v1/stations/{id}/summary`

Armazenamento temporal recomendado em UTC.

## 7. Dashboard

Dashboard público e desacoplado do banco, consumindo somente a API REST. Deve suportar métricas atuais, histórico, seleção de período, localização e estados de erro/ausência.

## 8. Validação

- não inventar valor em falha de leitura;
- marcar qualidade por métrica;
- validar timestamp e schema;
- não declarar unidade não sustentada;
- separar evidência simulada de evidência física;
- MQ-135 permanece raw/experimental até calibração;
- LDR permanece relativo até calibração;
- chuva não é mm até validação metrológica.

## 9. Segurança e configuração

SSID, senhas, tokens e credenciais não são versionados. Entradas externas são validadas; CORS é explícito; logs não expõem segredos.

## 10. Testes

Camadas: funções/drivers, sensores, serialização/contrato, backend, persistência, API, frontend, integração ponta a ponta, operação degradada e campo.

Até a chegada dos componentes, testes de firmware usam doubles/fixtures e não contam como validação física.

## 11. Governança

- mudanças relevantes exigem ADR;
- `main` representa integração estável;
- desenvolvimento ocorre em branch e PR;
- sem push direto na `main`;
- merge somente após revisão/checks;
- evidência deve declarar se é simulada ou física.

## 12. Pendências físicas

Permanecem TBD até os módulos reais estarem disponíveis:
- GPIOs definitivos;
- endereços I²C;
- níveis elétricos e alimentação;
- condicionamento do MQ-135;
- divisor/conversão do LDR;
- saída e comportamento do módulo de chuva;
- intervalos/periodicidades finais;
- estabilidade em bancada e campo.
