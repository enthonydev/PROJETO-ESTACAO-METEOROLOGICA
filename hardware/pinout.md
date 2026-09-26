# Pinout preliminar e mapa de interfaces

**Classificação:** PROJETADO / PENDENTE DE HARDWARE  
**Este documento não é montagem validada e não fixa GPIO definitivo.**

## Confirmado pela baseline

- O controlador previsto é um ESP32 DevKit V1.
- O barramento local previsto é I²C.
- O TCA9548A deve mediar os dois OLEDs SH1106.
- O canal 0 é destinado ao OLED meteorológico.
- O canal 1 é destinado ao OLED de relógio/calendário.
- BME280 e DS3231 pertencem conceitualmente ao subsistema local I²C.
- GPIOs, tensões, endereços e alimentação definitivos dependem da placa, módulos e datasheets reais.

## Mapa conceitual

| Sinal/função | Origem/destino | Interface | GPIO ESP32 | Alimentação | Estado |
|---|---|---|---|---|---|
| SDA | ESP32 ↔ barramento I²C | I²C | TBD | TBD | Pendente de validação física |
| SCL | ESP32 ↔ barramento I²C | I²C | TBD | TBD | Pendente de validação física |
| Canal 0 | TCA9548A → OLED meteorológico | I²C multiplexado | Seleção por comando I²C | TBD | Projetado |
| Canal 1 | TCA9548A → OLED relógio/calendário | I²C multiplexado | Seleção por comando I²C | TBD | Projetado |
| BME280 | Sensor → ESP32/TCA9548A | I²C | Pelo barramento | TBD | Pendente de hardware |
| DS3231 | RTC → ESP32/TCA9548A | I²C | Pelo barramento | TBD | Pendente de hardware |
| DHT22 | Sensor → ESP32 | Protocolo do componente | TBD | TBD | Pendente de decisão e hardware |
| BMP280 | Sensor ↔ ESP32 | I²C ou SPI | TBD | TBD | Pendente de decisão e hardware |
| MQ-135 | Sensor → ESP32 | ADC | TBD | TBD | Pendente de hardware/calibração |
| LDR | Divisor → ESP32 | ADC | TBD | TBD | Pendente de hardware |
| Pluviômetro | Sensor → ESP32 | Pulso/GPIO | TBD | TBD | Pendente de hardware/calibração |
| Wi-Fi | ESP32 ↔ rede | Wi-Fi | Integrado | N/A | Projetado; não executado no dispositivo |

## Proposto, sem aprovação final

- Usar um único barramento I²C lógico com seleção de canal do TCA9548A para os dois OLEDs.
- Manter BME280 e DS3231 no domínio I²C conforme a arquitetura conceitual.
- Reservar ADC/GPIO para MQ-135, LDR e pluviômetro somente depois de confirmar conflito com Wi-Fi, boot pins, restrições ADC e níveis elétricos.
- Evitar fixar ADC2 enquanto a utilização de Wi-Fi estiver prevista, até revisão da pinagem.

Essas são diretrizes de planejamento, não uma pinagem aprovada.

## TBD obrigatório

- GPIO SDA/SCL e GPIOs dos sensores adicionais.
- Endereços I²C efetivos dos módulos.
- Tensões de alimentação e níveis lógicos de cada módulo.
- Resistores de pull-up e sua compatibilidade com o conjunto do barramento.
- Modelo de pluviômetro e circuito de entrada.
- Modelo exato dos OLEDs e configuração de endereço.
- Existência, coexistência ou exclusão de DHT22/BMP280 em relação ao BME280.

## Critério para liberar pinout definitivo

O pinout somente poderá ser marcado como **CONFIRMADO** depois de:

1. modelos e datasheets reais serem confirmados;
2. requisitos e decisão dos POs sobre BME280 versus DHT22/BMP280 serem registrados;
3. alimentação e níveis elétricos serem revisados;
4. conflitos de GPIO/ADC/boot/Wi-Fi serem analisados;
5. o circuito ser montado e testado em bancada;
6. evidência do teste ser registrada.
