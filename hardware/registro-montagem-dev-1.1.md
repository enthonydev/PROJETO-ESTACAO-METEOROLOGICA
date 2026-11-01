# Registro de montagem e validação física — DEV 1.1

**Data do registro:** 2026-11-01  
**Origem das evidências:** montagem acompanhada e leituras informadas pelo operador; não houve nova inspeção visual nem novo teste instrumental nesta revisão.  
**Firmware físico:** Arduino/C++ (não MicroPython). Porta serial: 115200 baud. OLED SSD1306 128×64 em 0x3C.

## GPIOs validados

| Componente | Conexão ESP32 | Estado |
| --- | --- | --- |
| OLED SDA / SCL | GPIO21 / GPIO22 | Validado em bancada |
| DHT22 OUT | GPIO16 | Temperatura e umidade exibidas |
| Chuva DO | GPIO17 INPUT_PULLUP | HIGH=seco; LOW=água |
| LDR DO | GPIO5 INPUT | LOW=claro; HIGH=escuro |
| BMP280 | Sem conexão | Pinos não soldados |
| MQ-135 | Sem conexão | 5V; insuficiência de espaço/cabos |

## Percurso registrado na protoboard

Convenção: A–E e F–J de uma mesma linha compartilham contato; a fenda central os separa.

| Circuito | Percurso reportado |
| --- | --- |
| Alimentação 3V3 | ESP32 I47 → J47 → B31 → A31 → A6 → OLED E6 |
| Terra | ESP32 I48 → J48 → C30 → A30 → A5 → OLED E5 |
| OLED SCL | OLED E7 → A7 → A29 → B29 → J37 → I37 → I40 → J40 → J60 → ESP32 I60/GPIO22 |
| OLED SDA | OLED E8 → A8 → A32 → B32 → J57 → ESP32 I57/GPIO21 |
| DHT22 + / OUT / - | C31 (3V3) / J52 (GPIO16/I52) / D30 (GND) |
| Chuva VCC | módulo D16 → A16 → E31 (3V3) |
| Chuva GND | módulo D17 → A17 → B5 (GND) |
| Chuva DO | módulo D18 → A18 → A25 → B25 → J42 → I42 → J53 → GPIO17/I53 |
| Chuva AO | módulo D19; não conectado |
| LDR VCC | módulo G19 → J19 → B6 (3V3) |
| LDR GND | módulo G18 → J18 → C5 (GND) |
| LDR DO | módulo G17 → J17 → J35 → I35 → J54 → GPIO5/I54 |
| LDR AO | módulo G16; não conectado |

**Atenção:** furo E30 apresentou mau contato; não utilizar. Sensor de chuva inicialmente causou instabilidade na OLED por aterramento em E30. Posteriormente um jumper desconectado provocou falso `CHUVA: SIM`; reconexão restaurou o estado correto. O potenciômetro do módulo de chuva foi ajustado para alternância seco/molhado.

## Evidências físicas da DEV 1.1

- OLED exibiu simultaneamente temperatura, umidade, chuva e luz.
- DHT22: leitura real de 23,2 °C e 85,6–85,8% UR no log fornecido (sem aferição de precisão).
- Chuva: seca = HIGH / NAO; molhada = LOW / SIM; retorno ao seco = HIGH / NAO.
- LDR: coberto = HIGH / ESCURO; descoberto = LOW / CLARO.
- Diagnóstico do GPIO17 repetido a cada 5 segundos; log seco confirmou HIGH.
- 3V3 medido previamente em aproximadamente 3,30 V.
- Operador confirmou teste de regressão da DEV 1.1.

## Limitações e riscos

- O ensaio de LDR digital **não** aprova a medição relativa analógica requerida em HW-T08; `luminosity_pct=null` até futura validação.
- O módulo de chuva é experimental, não pluviômetro: `rain_mm=null` sempre neste firmware.
- GPIO5 é strapping; realizar teste de reinicialização com LDR em ambos os estados.
- MQ-135 requer alimentação de 5 V, análise do consumo e proteção das entradas ADC do ESP32; não foi conectado.
- BMP280 exige montagem/solda e confirmação de terminais.
- Fios soltos podem produzir leituras falsas; o `INPUT_PULLUP` não detecta todas as falhas físicas.
- Telemetria ponta a ponta **não validada fisicamente** até execução do teste USB/serial → backend → dashboard.
- Sem dados calibrados de MQ-135, não inferir ppm, índice de qualidade do ar ou pressão atmosférica.

## Testes do plano hardware

HW-T01 boot: observado funcionalmente; HW-T02 3V3: medição pontual; HW-T04 OLED: validado; HW-T05 DHT22: leitura funcional; HW-T09 chuva experimental digital: validado. HW-T08 **parcial** (apenas DO); HW-T03 permanece parcial (OLED, sem BMP280). Demais HW-Txx pendentes.

## Compatibilidade arquitetural

O repositório contém um firmware-base em MicroPython para o alvo MQTT, mas a montagem operacional utiliza Arduino/C++. A integração experimental pela USB serial serve como **ponte de validação**, não substitui o objetivo final MQTT/NTP nem a aprovação arquitetural dessa opção.
