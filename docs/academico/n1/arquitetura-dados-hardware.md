# Arquitetura, dados e hardware da N1

## 1. Objetivo e classificação

Este documento consolida os artefatos de arquitetura, backend, firmware, banco e hardware disponíveis na `main`. Documentação, código, CI e simulação não são tratados como validação física.

| Classificação | Aplicação |
|---|---|
| Implementado | Código, SQL ou documento versionado. |
| Validado em software | Comportamento exercitado por teste/CI sem hardware. |
| Simulado | Comportamento exercitado com doubles, fixtures ou estados sintéticos. |
| Projetado | Decisão arquitetural sem integração comprovada. |
| Pendente | Artefato/teste ainda não disponível. |
| Bloqueado | Conclusão depende de hardware, pinout, calibração ou evidência física. |

## 2. Arquitetura integrada

```text
DHT22 + BMP280 + MQ-135 + LDR + chuva experimental
                    ↓
             ESP32 / MicroPython
                    ↓
                Wi-Fi/MQTT
                    ↓
             Backend/FastAPI
                    ↓
               PostgreSQL
                    ↓
               API REST
                    ↓
             Dashboard Web
```

O ESP32 possui uma única OLED I²C 128x64. NTP é a fonte principal de sincronização temporal. A API meteorológica externa é complementar e não substitui sensores físicos.

A baseline física foi decidida no ADR-002. BME280 adicional, DS3231, segunda OLED e TCA9548A não fazem parte da baseline atual.

## 3. Backend e contrato

O backend disponível contém healthcheck e validação de telemetria. O contrato v1.0 permanece a fronteira de integração. MQTT, persistência runtime, consultas completas e dashboard continuam etapas posteriores quando ainda não houver evidência correspondente.

O campo `rain_mm` permanece no contrato por compatibilidade, porém o módulo de chuva da baseline não sustenta milímetros quantitativos sem método/fator validado. Nenhum valor deve ser inventado para preencher esse campo.

## 4. Modelo de dados

O DER inicial contém `stations`, `measurements` e `measurement_quality`. A migration representa o modelo versionado, mas sua existência não equivale a execução validada contra PostgreSQL.

## 5. Hardware e firmware

| Frente | Baseline/estado | Limite atual |
|---|---|---|
| Temperatura/umidade | DHT22 | driver e leitura física pendentes |
| Pressão | BMP280 | driver/endereço/leitura física pendentes |
| Qualidade do ar | MQ-135 raw | sem ppm até calibração |
| Luminosidade | LDR relativa | circuito/conversão física pendentes |
| Chuva | módulo experimental | sem `rain_mm` até método validado |
| Display | uma OLED I²C | endereço e operação física pendentes |
| Tempo | NTP | sem RTC dedicado; comportamento offline deve ser testado |
| Conectividade | Wi-Fi/MQTT | integração real pendente |
| Pinagem | interfaces documentadas | GPIO definitivo após módulos reais |

O firmware mantém abstrações de sensores, tempo, API externa e uma interface local única. Testes com doubles são evidência de software, não de montagem.

## 6. Consequências para a N1

A N1 pode demonstrar arquitetura, contrato, modelo, protótipo de software, testes e CI. Não pode declarar estação montada, precisão, calibração, funcionamento elétrico, chuva em milímetros ou teste de campo enquanto essas evidências não existirem.

## 7. Frente de hardware e decisão arquitetural

`hardware/bom.md`, `hardware/pinout.md`, `hardware/diagrams/interconexoes.md` e `hardware/plano-testes.md` registram a preparação de bancada. O ADR-002 encerrou a divergência de baseline: DHT22 + BMP280 são as fontes previstas de temperatura/umidade e pressão; o BME280 adicional foi removido.

O gate documental pode avançar. O gate físico permanece pendente da aquisição e chegada dos componentes.

## 8. Referências internas

- `docs/arquitetura/arquitetura-sistema.md`
- `docs/arquitetura/adr/ADR-002-adequacao-arquitetura-fisica-orcamento.md`
- `docs/arquitetura/coerencia-hardware-firmware-contrato.md`
- `hardware/bom.md`
- `hardware/pinout.md`
- `hardware/plano-testes.md`
- `firmware/tests/test_structure.py`
- `firmware/tests/test_tasks.py`
