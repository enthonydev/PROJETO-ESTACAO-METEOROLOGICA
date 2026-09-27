# ADR-002 — Adequação da arquitetura física por restrição orçamentária

- Status: Aceita
- Data: 2026-09-27
- Decisores: equipe do projeto
- Escopo: protótipo acadêmico da Estação Meteorológica Inteligente com ESP32

## Contexto

A baseline anterior incorporava componentes de interface e redundância que aumentavam o custo do protótipo: duas telas OLED, multiplexador TCA9548A, RTC DS3231 e BME280 adicional. Após revisão dos materiais acadêmicos do projeto e do orçamento disponível, foi definido que a prioridade deve permanecer no sensoriamento físico exigido para a estação, preservando temperatura, umidade, pressão atmosférica, qualidade do ar, luminosidade e precipitação/chuva.

O orçamento físico de referência passa a ser de até R$ 220,00 para a equipe, equivalente a até R$ 55,00 por integrante. O valor é requisito de planejamento e não substitui a validação dos componentes e das condições elétricas.

## Decisão

A baseline física do protótipo passa a utilizar:

- 1 ESP32 DevKit V1;
- 1 DHT22 para temperatura e umidade;
- 1 BMP280 para pressão atmosférica;
- 1 MQ-135 para resposta bruta relacionada à qualidade do ar;
- 1 módulo LDR para luminosidade;
- 1 módulo sensor de chuva para detecção/avaliação experimental de chuva;
- 1 OLED I2C 128x64 como interface local;
- protoboard, jumpers e alimentação compatível.

São removidos da baseline:

- BME280 adicional;
- RTC DS3231;
- segunda tela OLED;
- multiplexador TCA9548A.

A sincronização temporal será realizada prioritariamente por NTP quando houver conectividade. A ausência de RTC dedicado deve ser tratada como limitação operacional em condição offline.

A API meteorológica externa permanece complementar. Ela não substitui as medições realizadas pelos sensores físicos da estação.

## Precipitação

O módulo de chuva de baixo custo adotado nesta etapa não deve ser tratado como pluviômetro calibrado. Enquanto não existir mecanismo físico e fator de conversão validados experimentalmente, o sistema não deve afirmar que a leitura representa precipitação quantitativa em milímetros.

O contrato existente poderá manter compatibilidade com o campo de precipitação durante a transição, porém dados quantitativos em `rain_mm` somente poderão ser produzidos quando houver método de medição e calibração defensável. Até essa validação, a leitura do módulo deve ser identificada como experimental e não metrológica.

## Consequências

### Positivas

- preservação do sensoriamento físico central ao projeto acadêmico;
- redução do custo e da complexidade de montagem;
- eliminação do TCA9548A e do segundo display;
- eliminação da redundância DHT22/BMP280 versus BME280 adicional;
- menor quantidade de pontos de falha;
- arquitetura de firmware mais simples.

### Limitações

- sem RTC dedicado, a manutenção de horário correto durante longos períodos offline não é garantida;
- uma única tela concentra toda a interface local;
- o módulo de chuva não fornece, por si só, pluviometria calibrada em mm;
- MQ-135 deve permanecer como leitura bruta/experimental enquanto não houver calibração defensável;
- LDR fornece luminosidade relativa, não iluminância metrológica em lux sem calibração apropriada.

## Arquitetura resultante

```text
DHT22 ───────┐
BMP280 ──────┤
MQ-135 ──────┤
LDR ─────────┼──> ESP32 / MicroPython ──Wi-Fi──> MQTT ──> Backend ──> PostgreSQL
Sensor chuva ┘             │                                │
                           ├──> OLED local                  └──> API REST ──> Dashboard
                           ├──> NTP
                           └──> API meteorológica externa (complementar)
```

## Impactos obrigatórios

Esta decisão exige revisão coordenada de:

- BOM;
- pinout e mapa de interconexões;
- arquitetura do sistema;
- coerência hardware/firmware/contrato;
- firmware de sensores, tempo e display;
- testes de hardware e integração;
- matriz de rastreabilidade;
- documentação acadêmica N1.

Backend, banco de dados e fluxo principal de telemetria permanecem válidos, salvo ajustes semânticos necessários para representar corretamente a chuva experimental.

## Critério de encerramento

A adequação será considerada concluída quando documentação, firmware e testes não dependerem de BME280 adicional, DS3231, TCA9548A ou segunda OLED e quando a semântica das medições físicas estiver coerente com as capacidades reais dos componentes.
