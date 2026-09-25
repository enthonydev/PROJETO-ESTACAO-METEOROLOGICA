# Protótipo e casos de teste da N1

## 1. Objetivo e escopo

Este documento atende à task J-S3-03 da Sprint 3. Ele registra somente o protótipo de software, os fixtures e os testes presentes na `main`. Os estados “validado em software” e “simulado” não são apresentados como validação física.

## 2. Protótipo disponível

O protótipo atual é um skeleton integrado de software e dados, composto por:

1. aplicação FastAPI com healthcheck e validação de telemetria;
2. schema de payload v1.0 com estados de qualidade;
3. fixtures de telemetria válida, parcial e inválida;
4. serviços e modelos estruturais do firmware;
5. renderizadores de display que recebem estados processados;
6. DER e migration SQL iniciais;
7. script de validação do contrato;
8. documentação da arquitetura, requisitos e metodologia.

Este protótipo ainda não é uma estação física funcional. Não há evidência integrada de ESP32 executando o firmware, sensores conectados, broker MQTT, PostgreSQL em execução, dashboard ou teste de campo.

## 3. Casos de teste existentes

| ID documental | Caso | Arquivo | Estado da evidência |
|---|---|---|---|
| T-S3-01 | Healthcheck responde `200` e status `ok`. | `backend/tests/test_api.py::test_health` | Executado em software, sem hardware |
| T-S3-02 | Payload válido é aceito e normalizado com schema `1.0` e estação esperada. | `backend/tests/test_api.py::test_valid_payload_is_returned_normalized` | Executado em software com fixture |
| T-S3-03 | Payload parcial preserva valor nulo e marca qualidade como `error`. | `backend/tests/test_api.py::test_partial_payload_preserves_null_and_quality_error` | Executado em software com fixture |
| T-S3-04 | Payload inválido é rejeitado com HTTP 422. | `backend/tests/test_api.py::test_invalid_payload_is_rejected` | Executado em software com fixture |
| T-S3-05 | Falha de um driver não elimina a leitura válida de outro sensor. | `firmware/tests/test_structure.py::test_sensor_service_isolates_driver_failure` | Simulado com `FailingDriver`; não é teste físico |
| T-S3-06 | Renderer meteorológico recebe estado processado e envia view model ao display. | `firmware/tests/test_structure.py::test_weather_display_receives_processed_state` | Simulado com display fake |
| T-S3-07 | Renderer de relógio recebe estado temporal resolvido. | `firmware/tests/test_structure.py::test_clock_display_receives_resolved_time` | Simulado com display fake |
| T-S3-08 | Serviço converte tupla temporal sem colocar lógica NTP no display. | `firmware/tests/test_structure.py::test_time_service_converts_source_tuple_without_ntp_logic_in_display` | Validado em software; não testa NTP ou DS3231 |
| T-S3-09 | Contrato e fixtures são JSON válidos e compatíveis com as regras do repositório. | `scripts/validate_contract.py` e workflow de CI | Executado em software |

## 4. Testes planejados, mas ainda não executados

Os seguintes testes permanecem planejados ou bloqueados e não devem ser descritos como resultados obtidos:

| Teste planejado | Motivo do estado |
|---|---|
| Publicação e recebimento MQTT | Broker e integração de firmware ainda não comprovados |
| Persistência e consulta PostgreSQL | Não há evidência de execução do banco nesta Sprint |
| Reconexão Wi-Fi e operação offline | Depende de ESP32 e rede reais |
| NTP e fallback DS3231 | Depende de componentes e montagem físicos |
| Leitura de DHT22/BMP280/BME280/MQ-135/LDR/pluviômetro | Depende de sensores conectados e drivers validados |
| Teste de canais do TCA9548A e displays OLED | Depende de pinagem, endereços e hardware reais |
| Calibração e comparação com referência | Não há instrumento de referência nem protocolo executado |
| Dashboard, acessibilidade e mapa | Frontend ainda não implementado |
| Teste ponta a ponta | As camadas não estão integradas em execução real |
| Teste de campo | Não há montagem ou série física disponível |

## 5. Procedimento de reprodução do software

Os testes de backend devem ser executados a partir de `backend/` com as dependências de `backend/requirements.txt` instaladas e o pacote `app` no `PYTHONPATH`. Os testes de firmware estrutural devem ser executados a partir de `firmware/`, também sem placa conectada. O script `scripts/validate_contract.py` deve ser executado a partir da raiz do repositório.

A reprodução desses testes demonstra o comportamento dos módulos em software. Ela não demonstra consumo, latência física, cobertura Wi-Fi, precisão, estabilidade ambiental ou funcionamento da eletrônica.

## 6. Critério de evidência

Cada futura evidência deverá registrar ambiente, data, versão do código, entrada, procedimento, resultado, responsável e classificação. Fotografias, logs de placa, leituras de instrumento de referência e arquivos de medição somente poderão ser classificados como evidência física quando realmente existirem e forem vinculados ao procedimento correspondente.

## 7. Referências internas

[1]: ../../requisitos/matriz-rastreabilidade-n1.md "Matriz de rastreabilidade da N1"
[2]: ../../arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
[3]: ../../testes/README.md "Diretrizes de testes"
[4]: ../../../backend/tests/test_api.py "Testes da API"
[5]: ../../../firmware/tests/test_structure.py "Testes estruturais do firmware"
[6]: ../../../scripts/validate_contract.py "Validador do contrato"
