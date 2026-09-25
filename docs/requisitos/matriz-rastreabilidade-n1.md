# Matriz de rastreabilidade da N1

## 1. Objetivo e estado

Este documento atende à task J-S3-01 da Sprint 3. A matriz relaciona requisitos aos artefatos, testes e evidências efetivamente disponíveis na `main` após a integração técnica da Sprint 3.

A matriz diferencia implementação, teste executado em software, simulação, projeto e validação física. Nenhum resultado desta versão é apresentado como validação física. Não há pinagem validada, calibração, teste de bancada ou evidência física integrada ao repositório.

## 2. Legenda

| Estado | Significado |
|---|---|
| Documentado | Existe requisito ou artefato documental versionado. |
| Implementado | Existe código, SQL ou documento versionado na `main`. |
| Validado em software | Um teste executável ou inspeção reproduzível foi executado sem hardware físico. |
| Simulado | O comportamento foi exercitado com doubles, fixtures ou dados sintéticos. |
| Projetado | A arquitetura ou o modelo está definido, mas não há implementação ou validação correspondente. |
| Bloqueado | A conclusão depende de hardware, pinout, calibração, coordenadas ou evidência ainda inexistente. |
| Pendente | O artefato ou teste ainda não existe. |

## 3. Requisitos funcionais

| ID | Requisito resumido | Artefato na main | Teste/evidência existente | Estado real |
|---|---|---|---|---|
| RF-01 | Identificar estação por `station_id`. | Contrato v1.0; `backend/app/schemas/telemetry.py` | Fixture válida e teste de payload válido | Validado em software no backend; não é validação física |
| RF-02 | Adquirir temperatura e umidade. | `firmware/src/services/sensor_service.py`; arquitetura | `firmware/tests/test_structure.py` usa driver fake para temperatura e falha de umidade | Validado em software apenas para isolamento genérico; aquisição física bloqueada |
| RF-03 | Adquirir pressão atmosférica. | Requisito e arquitetura; driver físico não implementado | Nenhum teste de sensor de pressão | Projetado; bloqueado para validação física |
| RF-04 | Adquirir indicador de qualidade do ar. | Contrato com `air_quality_raw`; fundamentação sobre calibração | Nenhum teste de MQ-135 ou calibração | Projetado; interpretação/calibração bloqueadas |
| RF-05 | Adquirir luminosidade. | Contrato com `luminosity_pct`; arquitetura | Nenhum teste de LDR ou unidade | Projetado; hardware e unidade final pendentes |
| RF-06 | Adquirir precipitação. | Contrato com `rain_mm`; arquitetura | Nenhum teste de pluviômetro | Projetado; modelo e conversão bloqueados |
| RF-07 | Registrar timestamp e estação. | Contrato; `TelemetryPayload` | Fixture válida/parcial e validação de schema | Validado em software no backend; origem física do timestamp pendente |
| RF-08 | Validar leituras e qualidade no firmware. | `SensorService`; estados `ok` e `error` | Teste de isolamento de falha de driver | Validado em software para caso estrutural; faixas físicas não definidas |
| RF-09 | Publicar telemetria por Wi-Fi/MQTT. | Contrato e arquitetura; conectividade skeleton | Nenhum teste de publicação MQTT | Projetado; broker e firmware de publicação pendentes |
| RF-10 | Reconectar sem bloquear funções. | Arquitetura; `connectivity.py` skeleton | Nenhum teste de reconexão | Projetado; validação no ESP32 bloqueada |
| RF-11 | Validar telemetria no backend. | `backend/app/schemas/telemetry.py`; `telemetry_validation.py` | `backend/tests/test_api.py` e `backend/tests/test_contract.py`: válido, parcial, inválido, versão, campos extras e estação vazia | Validado em software |
| RF-12 | Persistir medição e qualidade. | DER e `database/migrations/001_schema_inicial.sql` | Inspeção de SQL; nenhum banco executado no CI atual | Implementado como modelo/migration; execução contra PostgreSQL e persistência runtime pendentes |
| RF-13 | Expor saúde, estações, última leitura, histórico e resumo. | `/health` e `/api/v1/telemetry/validate` implementados; endpoints restantes na arquitetura | Teste de healthcheck e validação | Parcialmente validado em software; endpoints de consulta pendentes |
| RF-14 | Exibir métricas atuais. | Requisito; frontend ainda sem implementação | Nenhum teste de interface | Pendente |
| RF-15 | Consultar histórico por período. | Endpoint previsto na arquitetura | Nenhum endpoint/teste integrado | Pendente |
| RF-16 | Representar localização aprovada. | Campos de localização no contrato e DER | Coordenadas reais inexistentes | Projetado; coordenadas e validação física bloqueadas |
| RF-17 | Exibir loading, erro e ausência de dados. | Requisito; frontend ainda sem implementação | Nenhum teste de interface | Pendente |
| RF-18 | Exibir estado meteorológico local e externo. | `WeatherDisplay` e `WeatherState` | Teste de renderer com estado preparado | Validado em software para renderer; API, sensores e display físico bloqueados |
| RF-19 | Exibir relógio e calendário. | `ClockDisplay` e `ClockState` | Teste de renderer com estado resolvido | Validado em software para renderer; OLED e RTC físicos bloqueados |
| RF-20 | Sincronizar NTP e manter DS3231 offline. | `TimeService.to_clock_state`; arquitetura | Teste de conversão de tupla, sem NTP/RTC real | Validado em software apenas para conversão; sincronização física bloqueada |
| RF-21 | Controlar displays por canais do TCA9548A. | Arquitetura; driver do multiplexador não implementado | Nenhum teste I2C | Projetado; pinout e hardware bloqueados |
| RF-22 | Isolar falhas parciais. | `SensorService` | Teste com `FailingDriver` | Validado em software para sensor fake; recuperação física pendente |
| RF-23 | Registrar falhas relevantes. | Estados e exceções no backend/firmware skeleton | Inspeção de estados; nenhum ensaio operacional | Parcialmente implementado; observabilidade integrada pendente |

## 4. Requisitos não funcionais

| ID | Requisito resumido | Artefato na main | Teste/evidência existente | Estado real |
|---|---|---|---|---|
| RNF-01 | Separar responsabilidades por camadas. | Estrutura de backend e firmware; arquitetura | Teste estrutural do firmware e inspeção | Validado em software por inspeção/teste estrutural |
| RNF-02 | Manter ciclos independentes. | `firmware/src/tasks/tasks.py`; arquitetura | Nenhum teste de concorrência no ESP32 | Implementado como skeleton/projetado; validação física pendente |
| RNF-03 | Operar de forma degradada. | Arquitetura; serviços skeleton | Falha de driver isolada em software | Validado em software parcialmente; operação offline física bloqueada |
| RNF-04 | Usar Python/FastAPI no backend. | `backend/app/main.py`; requirements | `test_health` e testes de endpoints | Validado em software |
| RNF-05 | Usar PostgreSQL com modelo compatível. | DER e migration SQL | Inspeção de schema; sem execução PostgreSQL no CI atual | Implementado como modelo; execução do banco e persistência runtime pendentes |
| RNF-06 | Usar política temporal única. | DER com `TIMESTAMPTZ`; arquitetura | Inspeção documental | Implementado/documentado; conversão apresentada em software |
| RNF-07 | Indexar estação e instante. | `measurements_station_measured_at_idx` | Inspeção da migration | Implementado em SQL; execução do banco pendente |
| RNF-08 | Separar dashboard do banco. | Arquitetura; frontend ainda sem implementação | Inspeção estrutural | Documentado; implementação frontend pendente |
| RNF-09 | Dashboard responsivo e acessível. | Requisitos e fundamentação WCAG | Nenhum teste de interface | Pendente |
| RNF-10 | Validar entradas externas. | Pydantic/schema e serviço de validação | Fixtures válida, parcial e inválida | Validado em software |
| RNF-11 | Não versionar segredos. | `.gitignore`; `SECURITY.md` | Inspeção do repositório | Documentado e verificado por inspeção |
| RNF-12 | Produzir logs úteis sem segredos. | Skeletons de backend/firmware | Nenhum ensaio de logs integrado | Pendente/parcial |
| RNF-13 | Versionar schema e compatibilidade. | JSON schema v1.0 e fixtures | `validate_contract.py` e checks CI | Validado em software |
| RNF-14 | Cobrir camadas de teste. | Testes backend, contrato e firmware estrutural | Pytest, `test_contract.py`, `test_structure.py` e `test_tasks.py`; camadas físicas ainda ausentes | Parcialmente validado em software |
| RNF-15 | Separar evidência física e simulada. | Metodologia, matriz e docs da Sprint 3 | Inspeção documental | Validado documentalmente; evidência física ainda inexistente |
| RNF-16 | Trabalhar por branch e PR. | Governança e branch da Sprint 3 | Histórico Git e PR | Aplicado |
| RNF-17 | Commits em português e autoria autorizada. | Histórico Git | Inspeção de autoria e mensagens | Aplicado |
| RNF-18 | Registrar mudanças relevantes em ADR. | ADR-001 e arquitetura | Inspeção documental | Documentado; ADR permanece sujeito à revisão prevista |
| RNF-19 | Manter rastreabilidade até N1/N2. | Esta matriz e documentos da N1 | Revisão cruzada | Em execução nesta Sprint 3 |
| RNF-20 | Garantir demonstração reproduzível. | Fixtures, testes e metodologia | Execução local dos testes e CI | Parcialmente validado em software; demonstração física pendente |

## 5. Evidências efetivamente existentes

### 5.1 Backend

A `main` contém um skeleton FastAPI com `GET /health` e `POST /api/v1/telemetry/validate`. Os testes verificam healthcheck, payload válido, payload parcial com qualidade de erro, rejeição de payload inválido, campos desconhecidos, versão de schema não suportada e `station_id` vazio. Esses testes são validações em software com fixtures; não demonstram conexão MQTT, persistência PostgreSQL ou operação em hardware.

### 5.2 Firmware

A `main` contém serviços, estados, renderers e tarefas estruturais. Os testes do firmware usam drivers e displays fake para verificar isolamento de falha de sensor, recebimento de estado processado pelos displays, conversão de estado temporal, delegação da tarefa de sensores, combinação de serviços de clima e relógio e entrega de estados às tarefas de display. Esses testes são simulações controladas e validações em software; não há hardware físico.

### 5.3 Banco de dados

A `main` contém um DER e uma migration SQL com as entidades `stations`, `measurements` e `measurement_quality`, chaves, estados de qualidade, timestamps `TIMESTAMPTZ` e índice `station_id + measured_at`. A migration é um artefato implementado no repositório, mas não há evidência nesta Sprint de execução contra um PostgreSQL real.

### 5.4 Ausências relevantes

Não existem evidências integradas de pinagem, montagem, leitura de sensores reais, calibração do MQ-135, conversão validada de chuva, coordenadas físicas, comunicação MQTT real, sincronização NTP/RTC em hardware, operação offline no ESP32, dashboard funcional ou teste de campo.

### 5.4 Auditoria de coerência

A auditoria `docs/testes/auditoria-coerencia-s3.md`, integrada na mesma `main`, compara implementação, arquitetura, contrato, modelo de dados e requisitos. Ela confirma que o contrato, os fixtures, a validação FastAPI e os serviços/estados de firmware estão validados em software, enquanto MQTT, PostgreSQL runtime, API de consultas, displays, sensores, Wi-Fi, dashboard e testes de campo permanecem projetados, pendentes ou bloqueados.

## 6. Referências

[1]: ../arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
[2]: ../contratos/contratos-integracao.md "Contratos de integração"
[3]: ../contratos/telemetria-v1.0.json "Contrato de telemetria v1.0"
[4]: ../arquitetura/adr/ADR-001-baseline-tecnica.md "ADR-001 — Baseline técnica do sistema"
[5]: ../academico/n1/metodologia-desenvolvimento.md "Metodologia de desenvolvimento da N1"
[6]: ../academico/n1/prototipo-e-testes.md "Protótipo e casos de teste da N1"
[7]: ../testes/auditoria-coerencia-s3.md "Auditoria de coerência técnica — Sprint 3"
