# Decisão de sensores — encerrada pelo ADR-002

**Status:** DECIDIDA  
**Referência:** ADR-002 — Adequação da arquitetura física por restrição orçamentária.

A decisão anteriormente pendente entre BME280 e DHT22 + BMP280 foi encerrada.

## Baseline aprovada

- DHT22: temperatura e umidade;
- BMP280: pressão atmosférica;
- MQ-135: indicador bruto de qualidade do ar;
- LDR: luminosidade relativa;
- módulo sensor de chuva: detecção/avaliação experimental;
- uma OLED I²C 128x64;
- ESP32 DevKit V1.

O BME280 adicional, DS3231, TCA9548A e a segunda OLED foram retirados da baseline.

## Consequência para o contrato

Os campos de temperatura, umidade, pressão, qualidade do ar e luminosidade permanecem compatíveis com a telemetria v1.0. O campo `rain_mm` exige tratamento cuidadoso: o módulo de chuva aprovado não constitui, por si só, pluviômetro calibrado. Valor quantitativo em mm somente poderá ser publicado depois de método e fator de conversão validados.

## Pendências que permanecem

A decisão de componentes não equivale a validação física. Continuam pendentes modelos efetivamente recebidos, datasheets, pinagem definitiva, níveis elétricos, calibração/interpretação de MQ-135 e LDR e caracterização do módulo de chuva.
