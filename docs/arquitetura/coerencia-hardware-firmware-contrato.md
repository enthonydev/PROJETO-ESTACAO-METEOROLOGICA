# Coerência entre hardware, firmware e contrato

**Classificação:** VALIDADO EM SOFTWARE para estrutura/contrato; PROJETADO para hardware; PENDENTE DE HARDWARE para integração física.

Este documento executa a revisão L-S4-02. Ele compara a arquitetura de hardware planejada, os diretórios de firmware e o contrato de telemetria v1.0 sem alterar a baseline de Enthony.

## Matriz de grandezas

| Campo do contrato | Grandeza | Componente previsto | Driver necessário | Unidade/semântica | Firmware atual | Estado da integração | Dependência |
|---|---|---|---|---|---|---|---|
| `temperature_c` | Temperatura | BME280 e/ou DHT22/BMP280 conforme decisão dos POs | Driver concreto do sensor escolhido | °C, se sustentado pelo datasheet/configuração | `SensorService` genérico; sem driver concreto | Projetado; software estrutural parcial | Modelo real, decisão de sensores, driver, teste físico |
| `humidity_pct` | Umidade relativa | BME280 e/ou DHT22 | Driver concreto do sensor escolhido | %, se sustentado | Campo aceito pelo contrato; serviço genérico | Projetado; software estrutural parcial | Modelo real, decisão de sensores, calibração/limites |
| `pressure_hpa` | Pressão atmosférica | BME280 e/ou BMP280 | Driver concreto do sensor escolhido | hPa, se conversão sustentada | Campo aceito pelo contrato; sem driver | Projetado | Modelo real, decisão de sensores e teste |
| `air_quality_raw` | Indicador bruto de qualidade do ar | MQ-135 | Driver ADC e condicionamento | valor bruto; não ppm | Campo do contrato; sem driver ADC | Projetado; calibração pendente | Circuito, alimentação, calibração e referência |
| `luminosity_pct` | Luminosidade relativa | LDR com divisor | Driver ADC e conversão documentada | %, somente após unidade/conversão aprovadas | Campo do contrato; sem driver ADC | Projetado | Divisor, GPIO/ADC, unidade e teste |
| `rain_mm` | Precipitação | Pluviômetro | Driver de pulsos/GPIO e contador | mm, somente com fator documentado | Campo do contrato; sem driver | Projetado | Modelo real, fator, calibração e teste |
| `timestamp` | Instante da amostra | DS3231, NTP e relógio do sistema conforme política | Driver RTC/NTP e composição temporal | ISO-8601 no payload; política UTC documentada | `TimeService` converte fonte injetada; não executa RTC/NTP | Validado em software somente para conversão | ESP32, DS3231, conectividade e teste offline |
| `quality.*` | Estado da métrica | Resultado do driver/validação | Regras de qualidade | `ok`, `suspect`, `invalid`, `error` | Backend e `SensorService` cobrem casos estruturais | Validado em software parcialmente | Faixas e comportamento físico ainda TBD |

## Estrutura atual do firmware

- `firmware/src/drivers/interfaces.py`: contratos abstratos de sensor, display e tempo; **não são drivers concretos**.
- `firmware/src/services/sensor_service.py`: lê drivers injetados e marca exceção como `None/error`; não conhece modelos físicos.
- `firmware/src/services/time_service.py`: usa fonte injetada e converte tupla em `ClockState`; não comprova NTP ou DS3231.
- `firmware/src/services/connectivity.py`: define fronteira `publish`, ainda sem implementação MQTT.
- `firmware/src/tasks/tasks.py`: representa unidades independentes de atualização; não implementa agendamento real no ESP32.
- `firmware/src/displays/`: renderiza estados em drivers injetados; testes usam display fake.
- `firmware/src/models/state.py`: representa snapshots, estados meteorológicos e de relógio.

## Correspondências confirmadas

1. Os seis campos de medição do contrato correspondem às grandezas previstas na arquitetura e nos requisitos.
2. O contrato preserva valores ausentes como `null` e exige estado de qualidade correspondente; isso está coberto por fixtures e testes backend.
3. A arquitetura separa aquisição, serviços, tasks, modelos e renderização; os testes estruturais exercitam essa separação sem hardware.
4. A arquitetura prevê TCA9548A, dois OLEDs SH1106, BME280 e DS3231; a documentação não deve transformar essa previsão em montagem validada.
5. O tópico `estacao/<station_id>/telemetry` e o schema v1.0 permanecem como fronteira de integração; não há publicação MQTT comprovada.

## Divergências e TBDs

- O firmware não possui drivers concretos para qualquer sensor, TCA9548A, SH1106 ou DS3231.
- O serviço de conectividade não publica MQTT.
- O contrato define campos, mas não resolve qual sensor concreto produzirá temperatura, umidade e pressão.
- O campo `luminosity_pct` não possui unidade/conversão aprovada.
- `rain_mm` não possui modelo de pluviômetro ou fator de conversão aprovado.
- `air_quality_raw` não autoriza inferir concentração/ppm.
- GPIOs, endereços I²C, tensões, pull-ups e alimentação são TBD.
- O comportamento de fallback entre fonte temporal primária e fallback precisa de implementação e teste próprios; a conversão de tupla existente não equivale a retenção offline.

## Dependências e itens bloqueados

**Pode avançar sem hardware:** documentação, matriz, contratos, testes estruturais com doubles, critérios de aceite e preparação dos procedimentos.  
**Pendente de decisão dos POs:** BME280 versus DHT22 + BMP280, simplificação/coexistência, unidades/conversões e escopo final.  
**Pendente de hardware:** modelos reais, alimentação, pinout, drivers concretos, leituras, I²C, displays, RTC, calibração, MQTT no dispositivo e integração de campo.

Nenhuma alteração foi feita no firmware ou no contrato nesta revisão.
