# Auditoria Sprint 5 — Frente de Software, Arquitetura e Integração Técnica

## Relatório final

| Task | Status | Branch | Arquivos | Testes/evidências | Dependências liberadas | Bloqueios | PR/commit | Revisão solicitada ao PO |
|---|---|---|---|---|---|---|---|---|
| E-S5-01 | **READY FOR N1** | `audit/sprint-5-fechamento-n1` | Relatório, escopo, insumos, auditorias e matriz documental corrigidos nesta branch | Backend 10/10, firmware 6/6, contrato OK, compilação OK, `git diff --check` OK, firmware sem dependências removidas | Arquitetura, contrato v1.0, backend de validação, firmware estrutural, modelo SQL, testes de software e documentação técnica | Nenhum bloqueador acadêmico da frente. Validações físicas e integrações ainda não implementadas seguem como backlog/N2 | Commits `9e5140c9f25758f4995e7c02a7d85af7a926745a` e `7bad7550a56f9cac5444f1fca21695e1bd06fe30`; PR #24 | Sim |

## 1. Resumo executivo

A auditoria foi realizada sobre a `main` no commit `067e01b`, que já contém a ADR-002 e a baseline física enxuta. A frente técnica está coerente para a N1: a arquitetura aceita utiliza ESP32 DevKit V1, DHT22, BMP280, MQ-135 bruto/experimental, LDR relativo, módulo de chuva experimental, uma OLED I²C 128x64 e NTP como referência temporal principal.

O contrato de telemetria v1.0 permanece estável. O backend implementado continua limitado ao healthcheck e à validação de payload. O firmware mantém serviços, estados, tasks, interfaces e uma única interface local, sem dependências funcionais de BME280 adicional, DS3231, TCA9548A, segunda OLED, `WeatherTask` ou `ClockTask`.

A auditoria não encontrou bloqueador acadêmico na frente de Enthony. A ausência de hardware físico não impede a N1, pois a validação de bancada, calibração, montagem, leitura real, teste de estabilidade, teste de campo e integração ponta a ponta foram reposicionados como validação futura/N2. Nenhum resultado físico foi inventado.

## 2. BLOQUEADORES DA N1

**Nenhum bloqueador da N1 foi encontrado na frente auditada.**

Os testes físicos HW-T01 a HW-T19 continuam não executados. Esse estado é correto e não impede o fechamento acadêmico da N1, porque a N1 exige que o hardware esteja projetado, especificado, documentado, integrado à arquitetura e acompanhado de plano de validação. A execução física pertence à etapa posterior/N2.

## 3. CORREÇÕES NECESSÁRIAS realizadas

A revisão corrigiu somente inconsistências objetivas:

1. O documento de stakeholders deixou de declarar duas OLEDs, DS3231 e TCA9548A como parte do produto e passou a refletir a única OLED e a baseline do ADR-002.
2. Os insumos técnicos passaram a referenciar ADR-002 em vez de ADR-001 e deixaram de citar SH1106, TCA9548A e DS3231 como limitações da baseline atual.
3. A auditoria da Sprint 3 foi atualizada para descrever a OLED única e os sensores aprovados, sem tratar componentes removidos como parte do sistema.
4. A auditoria acadêmica corrigiu a contagem de firmware de sete para seis testes.
5. O relatório N1 passou a indicar a Sprint 5 como versão documental e substituiu a antiga “decisão pendente entre BME280 e DHT22 + BMP280” pela decisão aceita no ADR-002.
6. A estrutura do documento N1 passou a referenciar o ADR-002 como decisão física aceita.

## 4. BACKLOG / N2

Os seguintes itens permanecem reais, mas não bloqueiam a N1:

- drivers concretos para DHT22, BMP280, MQ-135, LDR, módulo de chuva e OLED;
- validação de GPIO, níveis elétricos, alimentação e endereços I²C dos módulos recebidos;
- montagem e operação no ESP32;
- calibração ou caracterização do MQ-135 e do LDR;
- método e fator de conversão para chuva quantitativa;
- sincronização NTP real e teste da limitação offline sem RTC dedicado;
- publicação MQTT e reconexão no dispositivo;
- persistência e consultas em PostgreSQL runtime;
- endpoints completos de consulta e dashboard;
- teste ponta a ponta, estabilidade e campo;
- execução e aprovação dos testes HW-T01 a HW-T19.

## 5. Arquivos alterados

- `docs/requisitos/stakeholders-e-escopo.md`
- `docs/academico/n1/insumos-tecnicos-consolidacao.md`
- `docs/testes/auditoria-coerencia-s3.md`
- `docs/academico/n1/relatorio-n1.md`
- `docs/academico/n1/auditoria-consolidacao-n1.md`
- `docs/academico/n1/estrutura-documento-n1.md`
- `docs/academico/n1/auditoria-sprint-5-enthony.md`

O `README.md` foi auditado e não precisa de atualização nesta Sprint. Ele já descreve a baseline do ADR-002, o estado parcial do software e as pendências futuras sem declarar validação física.

## 6. Testes e evidências

Foram executados, sem hardware:

- `PYTHONPATH=backend python -m pytest backend/tests -q`: **10 passed**;
- `PYTHONPATH=firmware/src python -m pytest firmware/tests -q`: **6 passed**;
- `python scripts/validate_contract.py`: **OK** para os dois exemplos oficiais;
- `python -m compileall -q backend/app backend/tests firmware/src firmware/tests`: **OK**;
- `git diff --check`: **OK**;
- inspeção do firmware: nenhuma referência a BME280, DS3231, TCA9548A, SH1106, `WeatherTask`, `ClockTask`, `weather_display` ou `clock_display`;
- plano físico: HW-T01 a HW-T19 identificados como **NÃO EXECUTADO** e não aprovados.

Os testes usam fixtures, doubles e estados sintéticos. Portanto, são evidências de software/simulação e não evidências físicas.

## 7. Estado do contrato v1.0

O contrato permanece estável e coerente com o backend. Ele mantém `schema_version`, `station_id`, `timestamp`, `location`, `measurements` e `quality`, com estados `ok`, `suspect`, `invalid` e `error`.

A semântica das métricas foi preservada: `air_quality_raw` não é ppm calibrado, `luminosity_pct` é luminosidade relativa e `rain_mm` não recebe valor quantitativo sem método e fator validados. O tópico MQTT previsto permanece `estacao/<station_id>/telemetry`.

## 8. Estado da arquitetura após a auditoria

A arquitetura está coerente com o ADR-002. O fluxo principal continua:

```text
DHT22 + BMP280 + MQ-135 + LDR + chuva experimental
    → ESP32/MicroPython → Wi-Fi/MQTT → Backend/FastAPI
    → PostgreSQL → API REST → Dashboard Web
```

A interface local é uma única OLED I²C 128x64. NTP é a referência temporal principal. A API meteorológica externa é complementar. BME280 adicional, DS3231, segunda OLED e TCA9548A não fazem parte da baseline.

## 9. Estado da integração técnica

A integração está demonstrada em nível documental e estrutural de software. Contrato, validação FastAPI, fixtures, estados, tasks, renderização lógica, DER, migration, testes e CI estão alinhados.

A integração ponta a ponta ainda não existe em runtime. Não há consumidor MQTT, persistência PostgreSQL executável, endpoints completos de consulta, dashboard funcional ou execução no ESP32. Isso é backlog/N2 e não reduz o parecer de prontidão da frente para a N1.

## 10. Parecer final

**READY FOR N1 — frente de Enthony.**

O parecer é limitado à frente técnica auditada e não declara a Sprint 5 inteira concluída. A revisão do PO Enthony e a integração centralizada continuam necessárias. Não foi realizado merge na `main`.

## Referências

[1]: ../../../docs/arquitetura/adr/ADR-002-adequacao-arquitetura-fisica-orcamento.md "ADR-002 — Adequação da arquitetura física por restrição orçamentária"
[2]: ../../../docs/arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
[3]: ../../../docs/contratos/contratos-integracao.md "Contrato de integração da telemetria"
[4]: ../../../docs/contratos/telemetria-v1.0.json "Schema de telemetria v1.0"
[5]: ../../../docs/requisitos/matriz-rastreabilidade-n1.md "Matriz de rastreabilidade da N1"
[6]: ../../../hardware/plano-testes.md "Plano de testes de hardware e integração"
[7]: ../../../docs/testes/auditoria-coerencia-s3.md "Auditoria de coerência técnica da Sprint 3"
