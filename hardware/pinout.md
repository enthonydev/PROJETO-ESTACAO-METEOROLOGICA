# Pinout preliminar e mapa de interfaces

**Classificação:** BASELINE APROVADA / PINOS DEFINITIVOS PENDENTES DE HARDWARE  
**Decisão arquitetural:** ADR-002.

## Interfaces aprovadas

| Função | Componente | Interface | GPIO ESP32 | Estado |
|---|---|---|---|---|
| Temperatura/umidade | DHT22 | GPIO/protocolo DHT | TBD | Componente aprovado |
| Pressão | BMP280 | I²C | SDA/SCL TBD | Componente aprovado |
| Interface local | OLED 128x64 | I²C | SDA/SCL TBD | Uma única OLED aprovada |
| Qualidade do ar | MQ-135 | ADC | ADC1/TBD | Condicionamento elétrico pendente |
| Luminosidade | LDR | ADC | ADC1/TBD | Divisor e conversão pendentes |
| Chuva experimental | módulo de chuva | ADC/GPIO | TBD | Sem semântica de mm |
| Wi-Fi | ESP32 | integrado | N/A | Baseline |
| Tempo | NTP | Wi-Fi | N/A | Referência principal |

BMP280 e OLED podem compartilhar o mesmo barramento I²C desde que endereços, tensão e módulos reais sejam confirmados. Não existe mais dependência de TCA9548A.

## Diretrizes para pinagem

- priorizar entradas ADC1 para leituras analógicas que coexistirão com Wi-Fi;
- evitar GPIOs de strapping/boot sem análise explícita;
- não aplicar ao ADC tensão superior à suportada pelo ESP32;
- revisar a saída analógica do módulo MQ-135 antes da conexão;
- manter GND comum quando eletricamente apropriado;
- confirmar pull-ups do barramento I²C nos módulos reais.

## Removido pelo ADR-002

Não reservar pinos ou barramento para:

- BME280 adicional;
- DS3231;
- TCA9548A;
- segunda OLED.

## Critério para marcar pinout como CONFIRMADO

1. componentes reais recebidos;
2. datasheets/modelos conferidos;
3. níveis elétricos revisados;
4. GPIOs revisados contra boot, ADC e Wi-Fi;
5. montagem em bancada concluída;
6. leituras e barramento testados;
7. evidências registradas.

Até lá, GPIOs permanecem TBD de forma intencional.
