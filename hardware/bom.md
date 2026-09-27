# Matriz de hardware e BOM

**Classificação:** BASELINE APROVADA / PENDENTE DE HARDWARE  
**Decisão arquitetural:** ADR-002.

A baseline física foi simplificada por restrição orçamentária sem remover o sensoriamento ambiental central. O teto de planejamento é de **R$ 220,00 para o protótipo (R$ 55,00 por integrante)**. Preços de compra são variáveis e não constituem especificação técnica.

| Componente | Qtd. | Função | Interface prevista | Estado |
|---|---:|---|---|---|
| ESP32 DevKit V1 | 1 | Controle, aquisição e Wi-Fi | GPIO, ADC, I²C, Wi-Fi | Aprovado; validação física pendente |
| DHT22 | 1 | Temperatura e umidade | GPIO/protocolo DHT | Aprovado; validação física pendente |
| BMP280 | 1 | Pressão atmosférica | I²C | Aprovado; validação física pendente |
| MQ-135 | 1 | Indicador bruto de qualidade do ar | ADC + condicionamento | Aprovado; calibração/validação pendentes |
| Módulo LDR | 1 | Luminosidade relativa | ADC | Aprovado; conversão/validação pendentes |
| Módulo sensor de chuva | 1 | Detecção/avaliação experimental de chuva | ADC/GPIO conforme módulo | Aprovado; não é pluviômetro calibrado |
| OLED I²C 128x64 | 1 | Interface local | I²C | Aprovado; modelo/endereço real pendentes |
| Protoboard + jumpers + alimentação | 1 conjunto | Prototipagem | — | Aprovado; conjunto real pendente |

## Componentes removidos da baseline

- BME280 adicional;
- DS3231;
- segunda OLED;
- TCA9548A.

## Semântica obrigatória

- DHT22 é a fonte prevista de temperatura e umidade.
- BMP280 é a fonte prevista de pressão.
- MQ-135 permanece como leitura bruta/experimental; não declarar ppm sem calibração defensável.
- LDR representa luminosidade relativa; não declarar lux sem calibração apropriada.
- O módulo de chuva não autoriza declarar precipitação em mm. `rain_mm` só poderá receber valor quantitativo após método e fator de conversão validados.
- NTP é a referência temporal principal quando houver conectividade.
- A API meteorológica externa é complementar e não substitui os sensores físicos.

## Pendências para fechamento elétrico

1. Confirmar fabricantes/modelos exatos recebidos e respectivos datasheets.
2. Confirmar tensão e níveis lógicos de cada módulo.
3. Fixar GPIOs após revisão de boot pins, ADC e coexistência com Wi-Fi.
4. Confirmar endereço I²C do BMP280 e da OLED.
5. Definir condicionamento seguro do MQ-135 para o ADC do ESP32.
6. Definir circuito do LDR.
7. Confirmar a saída disponível no módulo de chuva adquirido.

Nenhum item é considerado validado fisicamente até montagem e evidência de bancada.
