# Auditoria de coerência técnica — Sprint 3

## Escopo e método

Esta auditoria compara a implementação existente com a arquitetura aprovada, o contrato de telemetria v1.0, o modelo de dados e os requisitos funcionais. O objetivo é distinguir claramente o que está implementado e validado em software do que permanece apenas projetado ou bloqueado por hardware, infraestrutura ou integração ainda não desenvolvida.

## Estado por componente

| Componente | Estado | Evidência e limite |
|---|---|---|
| Contrato JSON de telemetria v1.0 | Implementado; validado em software | `docs/contratos/telemetria-v1.0.json`, exemplos oficiais e `scripts/validate_contract.py`. |
| Fixtures backend válida, parcial e inválida | Implementado; validado em software | Fixtures em `backend/tests/fixtures/` cobertas por testes automatizados. Não são evidências físicas. |
| Validação FastAPI | Implementado; validado em software | `POST /api/v1/telemetry/validate` valida o payload e `GET /health` responde. Não há ingestão MQTT. |
| Ingestão MQTT | Projetado; pendente | O tópico está documentado, mas não existe consumidor MQTT implementado nesta Sprint. |
| Persistência PostgreSQL | Projetado | A migration e o DER existem, mas não há conexão, execução de migration ou teste contra PostgreSQL nesta Sprint. |
| API REST de consultas | Projetado; pendente | Os endpoints de consulta estão na arquitetura, mas ainda não foram implementados. |
| Serviços e estados de firmware | Implementado; validado em software | Serviços, modelos, tasks e renderizadores são exercitados sem hardware físico. |
| Interfaces de drivers | Implementado como abstração | Os contratos de driver existem; não há drivers concretos nem GPIO. |
| Displays SH1106/TCA9548A | Bloqueado | A renderização recebe estado processado, mas integração elétrica e validação física dependem do hardware. |
| BME280, DS3231 e sensores | Bloqueado | Não há pinagem, drivers concretos, calibração ou medições físicas disponíveis. |
| Wi-Fi/MQTT no ESP32 | Projetado; bloqueado fisicamente | A arquitetura e a interface de conectividade existem; a execução embarcada depende de hardware e infraestrutura. |
| Dashboard | Pendente | Não está implementado nesta branch/tarefa. |

## Coerência com a arquitetura

A implementação mantém a separação definida na baseline: modelos representam estado, serviços obtêm ou processam dados, tasks coordenam atualizações e displays apenas renderizam o estado recebido. Os renderizadores não importam API, NTP ou sensores diretamente.

A ausência de MQTT, persistência, endpoints de consulta e dashboard é uma lacuna de implementação, não uma alteração da arquitetura. Nenhuma tecnologia baseline, contrato versionado ou fluxo aprovado foi alterado nesta Sprint.

## Coerência com o contrato

A validação FastAPI aceita somente `schema_version` `1.0`, exige `station_id`, timestamp, localização, medições e qualidade, rejeita campos extras e preserva valores `null` com estado de qualidade correspondente. O payload parcial não é convertido silenciosamente em zero.

O contrato documenta transporte MQTT, mas o backend atual ainda não implementa a ingestão. Portanto, não há evidência de integração MQTT nesta auditoria.

## Coerência com o modelo de dados

O modelo relacional projetado contém `stations`, `measurements` e `measurement_quality`, alinhados às entidades do contrato e aos requisitos de identificação, instante da medição e qualidade individual. A correspondência é de projeto; ainda não foi verificada por execução contra PostgreSQL.

## Requisitos observáveis nesta Sprint

| Requisito | Estado nesta Sprint | Observação |
|---|---|---|
| RF-01, RF-07, RF-08, RF-11 | Implementado; validado em software | Identificação, timestamp, qualidade e validação de schema são cobertos pelo modelo e pelos testes. |
| RF-02 a RF-06 | Projetado; bloqueado para validação física | O contrato aceita as métricas, mas aquisição, conversão e calibração dependem dos componentes reais. |
| RF-09 e RF-10 | Projetado; pendente/bloqueado | MQTT e reconexão ainda não foram implementados nem testados em ESP32. |
| RF-12 | Projetado | Migration e modelo existem; persistência executável ainda não. |
| RF-13 | Parcialmente implementado | Somente `GET /health` e validação de payload existem; consultas REST estão pendentes. |
| RF-18 a RF-22 | Estrutura parcial validada em software; validação física bloqueada | Há estados, tasks e renderizadores desacoplados, sem prova de funcionamento em displays ou sensores reais. |
| RF-23 | Parcialmente implementado | Falhas de drivers são isoladas no serviço de sensores; logging operacional completo ainda está pendente. |

## Conclusão

A Sprint 3 entrega testes executáveis, CI para artefatos existentes, integração estrutural das interfaces de firmware e auditoria de coerência. Ela não conclui a integração MQTT, a persistência, o dashboard ou a validação física. O Gate da Sprint não é declarado concluído por esta entrega; a revisão centralizada deve avaliar as dependências e as demais frentes.
