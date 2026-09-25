# Insumos técnicos para consolidação da N1

## 1. Estado geral

A `main` contém uma baseline técnica consistente entre arquitetura, contrato de telemetria, skeleton de backend, skeleton estrutural de firmware, modelo inicial de dados, testes automatizados e CI. Esses artefatos demonstram comportamento de software e organização técnica. Eles ainda não demonstram uma estação física integrada.

A consolidação acadêmica deve manter essa distinção. MQTT real, PostgreSQL em execução, dashboard funcional, sensores, displays, GPIO, calibração e montagem permanecem pendentes ou bloqueados quando exigem infraestrutura ou hardware que não estão disponíveis.

## 2. Classificação dos insumos

| Insumo | Estado atual | Evidência disponível | Limite da afirmação |
|---|---|---|---|
| Arquitetura do sistema | Projetado e documentado | `docs/arquitetura/arquitetura-sistema.md` e ADR-001 | A arquitetura não comprova integração executada. |
| Contrato de telemetria v1.0 | Implementado e validado em software | Schema JSON, exemplos oficiais e `scripts/validate_contract.py` | Não comprova publicação MQTT ou leitura física. |
| Validação de payload no backend | Implementado e validado em software | `GET /health`, `POST /api/v1/telemetry/validate` e testes FastAPI | Não há ingestão MQTT, persistência ou endpoints de consulta. |
| Fixtures de telemetria | Simulado e validado em software | Payloads válido, parcial e inválido em `backend/tests/fixtures/` | Os dados são sintéticos e não são medições de sensores. |
| Skeleton estrutural de firmware | Implementado e validado em software | Serviços, estados, tasks, interfaces, renderizadores e testes | Não há execução no ESP32 nem driver físico. |
| Interfaces de drivers | Implementado como abstração | `firmware/src/drivers/interfaces.py` | GPIO, pinagem e periféricos concretos permanecem bloqueados. |
| Renderizadores de display | Implementado e simulado em software | Testes com display fake e estado processado | Não comprova OLED, SH1106, TCA9548A ou operação elétrica. |
| Serviço de sensores | Implementado e simulado em software | Teste com driver válido e driver que falha | Não comprova DHT22, BMP280/BME280, MQ-135, LDR ou pluviômetro. |
| Serviço de tempo | Implementado e validado em software | Conversão de estado temporal e testes estruturais | Não comprova NTP real, DS3231 ou operação offline no ESP32. |
| Modelo relacional e DER | Projetado e implementado como artefato SQL | Migration, DER e restrições versionadas | Não houve execução contra PostgreSQL. |
| Persistência | Pendente | Não há conexão ou repositório executável | Não deve ser apresentada como implementada. |
| API REST de consulta | Pendente | Endpoints estão previstos na arquitetura | Somente healthcheck e validação de payload existem. |
| CI | Implementado e validado por execução local | Workflow executa contrato, backend, firmware e compilação | O CI não produz evidência física. |
| Auditoria técnica | Implementado e validado por inspeção | `docs/testes/auditoria-coerencia-s3.md` | A auditoria registra limites; não substitui testes ausentes. |
| Dashboard | Pendente | Não há implementação frontend integrada | Não há telas ou consultas demonstráveis. |
| Hardware e montagem | Bloqueado | Não há pinout, montagem ou logs de bancada versionados | Não há validação física, calibração ou medição real. |

## 3. Coerência entre os artefatos

A arquitetura define o fluxo `Sensores → ESP32/MicroPython → Wi-Fi → MQTT → Backend/FastAPI → PostgreSQL → API REST → Dashboard Web`. O repositório contém os contratos e os skeletons das camadas, mas não a execução ponta a ponta desse fluxo.

O contrato v1.0 está alinhado ao modelo Pydantic usado pelo endpoint de validação. Payloads parciais preservam `null` e registram o estado de qualidade correspondente. Campos desconhecidos, versão não suportada, timestamp inválido e identificação vazia são rejeitados pelos testes aplicáveis.

A migration SQL representa `stations`, `measurements` e `measurement_quality`, que correspondem à identificação da estação, ao instante da medição e à qualidade por métrica previstos no contrato e nos requisitos. A correspondência é de projeto e de artefato versionado. Sem uma instância PostgreSQL, não se deve afirmar que a persistência funciona em runtime.

O firmware estrutural respeita a separação segundo a qual serviços obtêm ou processam dados, tasks coordenam atualizações, modelos representam estados e displays recebem estado processado. Os testes usam doubles e dados sintéticos. Essa evidência é classificada como **simulada** e **validada em software**, nunca como física.

## 4. Evidências disponíveis para a N1

As evidências reproduzíveis são os testes automatizados do backend e do firmware, a validação do contrato, a compilação Python, a inspeção do SQL, o workflow de CI e a auditoria de coerência. Elas sustentam afirmações sobre o comportamento dos módulos em software.

Não existem evidências integradas de broker MQTT, banco PostgreSQL em execução, dashboard, placa ESP32, sensores, displays, pinagem, calibração, montagem ou teste de campo. Esses itens devem aparecer na N1 como **pendentes** ou **bloqueados**, conforme a dependência específica.

## 5. Orientação de redação para a N1

É adequado afirmar que existe um protótipo de software com contrato versionado, validação FastAPI, fixtures, modelo relacional, skeleton estrutural de firmware, testes e CI reproduzíveis. Não é adequado afirmar que a estação está montada, que os sensores foram validados, que a telemetria MQTT foi transmitida, que o PostgreSQL recebeu medições ou que os displays funcionam fisicamente.

Quando a N1 apresentar resultados, cada resultado deve informar se é **projetado**, **implementado**, **simulado**, **validado em software**, **pendente** ou **bloqueado**. A classificação deve permanecer próxima da afirmação correspondente.

## 6. Referências internas

[1]: ../../arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
[2]: ../../contratos/contratos-integracao.md "Contrato de integração da telemetria"
[3]: ../../contratos/telemetria-v1.0.json "Schema de telemetria v1.0"
[4]: ../../../backend/app/main.py "Aplicação FastAPI"
[5]: ../../../database/diagrams/der-inicial.md "DER técnico inicial"
[6]: ../../../database/migrations/001_schema_inicial.sql "Migration inicial do banco"
[7]: ../../../firmware/src/main.py "Composição inicial do firmware"
[8]: ../../testes/auditoria-coerencia-s3.md "Auditoria de coerência técnica da Sprint 3"
[9]: ../../../.github/workflows/docs-check.yml "CI de documentação, contrato e código"
