# Arquitetura, dados e hardware da N1

## 1. Objetivo e classificação da evidência

Este documento atende à task J-S3-02 da Sprint 3. Ele consolida no material acadêmico os artefatos de arquitetura, backend, firmware e banco de dados efetivamente presentes na `main` após a integração da Sprint 2.

A classificação usada é:

| Classificação | Aplicação nesta versão |
|---|---|
| Implementado | Código, SQL ou documento versionado na `main`. |
| Validado em software | Comportamento exercitado por teste local ou CI, sem hardware. |
| Simulado | Comportamento exercitado com fixtures, doubles ou estados sintéticos. |
| Projetado | Decisão arquitetural ou skeleton sem integração comprovada. |
| Pendente | Artefato ainda não disponível. |
| Bloqueado | Conclusão depende de hardware, pinout, calibração ou evidência física. |

Documentação, código e teste de software não são tratados como validação física.

## 2. Arquitetura integrada

A baseline integrada descreve o seguinte fluxo:

```text
Sensores → ESP32/MicroPython → Wi-Fi → MQTT → Backend/FastAPI → PostgreSQL → API REST → Dashboard Web
```

O ESP32 também possui uma frente local de visualização, com dois displays OLED mediados pelo TCA9548A. A arquitetura diferencia a interface embarcada da interface web pública. A API meteorológica externa complementa a tela local e não substitui os sensores físicos.

Na `main`, a separação de camadas está representada por:

- `firmware/src/models/`, para estados internos;
- `firmware/src/services/`, para aquisição, conectividade, tempo e API externa;
- `firmware/src/displays/`, para renderização de estados;
- `firmware/src/tasks/`, para tarefas estruturais;
- `backend/app/api/`, `schemas/`, `services/` e `core/`, para a aplicação FastAPI;
- `database/diagrams/` e `database/migrations/`, para o modelo persistente.

Essa separação foi verificada por inspeção estrutural e pelos testes existentes. Ainda não há integração ponta a ponta comprovada entre firmware, broker, backend, banco e dashboard.

## 3. Backend e contrato de telemetria

O backend implementado contém `GET /health` e `POST /api/v1/telemetry/validate`. O endpoint de validação recebe um objeto JSON, aplica o schema `TelemetryPayload` e retorna erro HTTP 422 para payload inválido. A própria implementação informa que a validação não persiste dados e que a ingestão MQTT será adicionada posteriormente.

O contrato v1.0 define `schema_version`, `station_id`, `timestamp`, localização, medições e qualidade por métrica. O tópico MQTT previsto é `estacao/<station_id>/telemetry`. A manutenção da versão do schema é uma decisão implementada no contrato e verificada pelos fixtures e pelo script de validação.

Os endpoints de estações, última leitura, histórico e resumo permanecem como baseline arquitetural, não como implementação comprovada nesta etapa.

## 4. Modelo de dados

O DER inicial contém três entidades principais:

| Entidade | Papel | Estado |
|---|---|---|
| `stations` | Identidade, código, nome, coordenadas, estado ativo e timestamps | Implementado na migration SQL |
| `measurements` | Instante medido e valores ambientais associados à estação | Implementado na migration SQL |
| `measurement_quality` | Estado e motivo por métrica da medição | Implementado na migration SQL |

A relação entre estação e medição é de um para muitos. Cada medição pertence a uma estação existente. A qualidade é registrada por métrica, com estados `ok`, `suspect`, `invalid` e `error`. O índice principal é composto por `station_id` e `measured_at`, e os timestamps são armazenados com `TIMESTAMPTZ` conforme a política de manter UTC no armazenamento e converter somente na apresentação.

O modelo inicial não define faixas físicas, fator de conversão da chuva, calibração do MQ-135 ou coordenadas reais. Essas lacunas são intencionais e devem continuar registradas como pendências até que existam decisões e evidências adequadas.

## 5. Hardware e firmware

A arquitetura projeta ESP32 DevKit V1, MicroPython, Wi-Fi, DHT22, BMP280/BME280, MQ-135, LDR, pluviômetro, DS3231, TCA9548A e dois OLEDs SH1106. O firmware versionado contém interfaces e serviços estruturais, estados, renderizadores e tarefas, mas não contém uma evidência de montagem, pinagem validada ou execução no dispositivo físico.

A distinção atual é:

| Frente | O que existe | O que continua bloqueado |
|---|---|---|
| Sensores | Contrato, arquitetura e serviço estrutural | Leituras físicas, datasheets aplicados, calibração e faixas finais |
| Displays | Renderers e estados testados com doubles | I2C, canais do TCA9548A, endereços, brilho e operação física |
| Tempo | Conversão de tupla para estado de relógio | NTP real, DS3231 real e recuperação offline no ESP32 |
| Conectividade | Estrutura de serviço e arquitetura Wi-Fi/MQTT | Broker, publicação, reconexão e teste de disponibilidade |
| Pinagem | Relações arquiteturais descritas | GPIO definitivo, conflitos ADC2/Wi-Fi, montagem e validação |
| Pluviometria | Campo `rain_mm` no contrato | Modelo do pluviômetro, fator de conversão e calibração |
| Qualidade do ar | Campo `air_quality_raw` e estados | Calibração e interpretação do MQ-135 |

Portanto, o texto acadêmico deve usar “projetado” ou “previsto” para a composição física e “validado em software” para os testes com doubles. Não deve usar “estação montada”, “medição validada” ou “calibração realizada”.

## 6. Consequências para a N1

A N1 já possui uma arquitetura coerente e um modelo de dados inicial implementado no repositório. A validação disponível é estrutural e de software. A integração física, a operação degradada real, a comunicação MQTT, a persistência em PostgreSQL, o dashboard e os testes de campo permanecem como pendências ou bloqueios conforme a matriz de rastreabilidade.

A ausência de evidência física não impede a apresentação do projeto como protótipo de software e arquitetura. Ela impede apenas conclusões sobre exatidão dos sensores, confiabilidade da estação, autonomia, representatividade espacial e funcionamento da montagem no ambiente real.

## 7. Referências internas

[1]: ../../arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
[2]: ../../contratos/contratos-integracao.md "Contratos de integração"
[3]: ../../contratos/telemetria-v1.0.json "Contrato de telemetria v1.0"
[4]: ../../arquitetura/adr/ADR-001-baseline-tecnica.md "ADR-001 — Baseline técnica do sistema"
[5]: ../../requisitos/matriz-rastreabilidade-n1.md "Matriz de rastreabilidade da N1"
[6]: ../../../backend/app/main.py "Ponto de entrada do backend FastAPI"
[7]: ../../../database/diagrams/der-inicial.md "DER técnico inicial"
[8]: ../../../firmware/tests/test_structure.py "Testes estruturais do firmware"
