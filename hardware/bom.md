# Matriz de hardware e BOM

**Classificação deste artefato:** PROJETADO / PENDENTE DE HARDWARE  
**Estado de disponibilidade:** não confirmado nesta versão.  
**Regra:** `TBD` significa que a informação depende de modelo real, datasheet confirmado, decisão dos POs ou validação física.

Esta matriz consolida os componentes mencionados na arquitetura, nos requisitos e no plano N1 de Luan. Ela não comprova aquisição, disponibilidade, montagem, endereço, tensão ou pinagem.

| Componente | Função | Quantidade | Modelo | Requisito relacionado | Interface prevista | Alimentação/tensão | Endereço | Fonte/datasheet | Disponibilidade | Implementação atual | Estado de teste | Validação física | Observações |
|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|
| ESP32 DevKit | Controlador, aquisição e conectividade | 1 | ESP32 DevKit V1, conforme baseline | RF-01 a RF-10; RNF-01 a RNF-03 | GPIO, ADC, I²C, Wi-Fi | TBD conforme placa real | N/A | [Espressif ESP32 Series Datasheet](https://documentation.espressif.com/esp32_datasheet_en.html) | Não confirmada | Firmware estrutural | Não executado | Pendente de hardware | GPIO, ADC, boot pins, alimentação e estabilidade ainda precisam ser conferidos na placa real. |
| TCA9548A | Multiplexação do barramento I²C para os dois displays | 1 | TCA9548A, módulo exato TBD | RF-21/22; RNF-03 | I²C | TBD conforme módulo real | TBD conforme configuração do módulo | [Texas Instruments TCA9548A](https://www.ti.com/product/TCA9548A) | Não confirmada | Apenas arquitetura | Não executado | Pendente de hardware | Canais conceituais: CH0 meteorologia e CH1 relógio/calendário. |
| OLED SH1106 | Display meteorológico | 1 | SH1106 1,3\", 128×64, módulo TBD | RF-18/22 | I²C via TCA9548A | TBD | TBD conforme módulo real | Datasheet do fabricante do módulo real: TBD | Não confirmada | Renderer com display fake | Não executado | Pendente de hardware | O endereço e a compatibilidade elétrica dependem do módulo real. |
| OLED SH1106 | Display relógio/calendário | 1 | SH1106 1,3\", 128×64, módulo TBD | RF-19/21/22 | I²C via TCA9548A | TBD | TBD conforme módulo real | Datasheet do fabricante do módulo real: TBD | Não confirmada | Renderer com display fake | Não executado | Pendente de hardware | Deve operar em canal independente do display meteorológico. |
| BME280 | Temperatura, umidade e pressão para o subsistema local | 1 | BME280, módulo TBD | RF-02/03/18; RNF-03 | I²C, endereço TBD | TBD conforme módulo real | TBD conforme SDO/módulo | [Bosch BME280 Datasheet](https://www.bosch-sensortec.com/products/environmental-sensors/humidity-sensors-bme280/) | Não confirmada | Serviço genérico de sensores | Não executado | Pendente de hardware | A coexistência com DHT22/BMP280 é uma decisão pendente dos POs. |
| DS3231 | Referência temporal local durante indisponibilidade de internet | 1 | DS3231, módulo TBD | RF-20/22; RNF-03 | I²C | TBD conforme módulo real | TBD conforme módulo | [Analog Devices DS3231](https://www.analog.com/en/products/ds3231.html) | Não confirmada | Serviço temporal por fonte injetada | Não executado | Pendente de hardware | NTP/RTC real, retenção temporal e correção ainda não foram testados. |
| DHT22 | Temperatura e umidade conforme baseline acadêmica | 1 | DHT22, módulo TBD | RF-02 | GPIO/protocolo do componente | TBD conforme datasheet/módulo | N/A | Datasheet do fabricante do modelo real: TBD | Não confirmada | Não há driver concreto | Não executado | Pendente de decisão e hardware | Não excluir sem decisão conjunta Luan/Enthony/James. |
| BMP280 | Pressão e temperatura conforme baseline acadêmica | 1 | BMP280, módulo TBD | RF-03 | I²C ou SPI, TBD | TBD conforme datasheet/módulo | TBD se I²C | [Bosch BMP280 Datasheet](https://www.bosch-sensortec.com/products/environmental-sensors/pressure-sensors/bmp280/) | Não confirmada | Não há driver concreto | Não executado | Pendente de decisão e hardware | Não excluir sem decisão conjunta Luan/Enthony/James. |
| MQ-135 | Indicador bruto de qualidade do ar | 1 | MQ-135, módulo TBD | RF-04/08; RNF-10 | ADC, condicionamento TBD | TBD conforme módulo e circuito | N/A | Datasheet do fabricante do modelo real: TBD | Não confirmada | Campo `air_quality_raw` no contrato | Não executado | Pendente de hardware/calibração | Não declarar ppm sem método de calibração defensável. |
| LDR | Luminosidade relativa | 1 | LDR e divisor, modelo TBD | RF-05 | ADC | TBD conforme divisor e ADC | N/A | Datasheet do componente real: TBD | Não confirmada | Campo `luminosity_pct` no contrato | Não executado | Pendente de hardware | Unidade e conversão ainda não definidas. |
| Pluviômetro | Precipitação | 1 | Modelo e mecanismo TBD | RF-06/08 | Pulso/GPIO, TBD | TBD | N/A | Datasheet do modelo real: TBD | Não confirmada | Campo `rain_mm` no contrato | Não executado | Pendente de hardware/calibração | Fator de conversão para mm não definido. |

## Decisões pendentes dos POs

1. Confirmar se BME280 coexistirá com DHT22 e BMP280 ou se haverá uma decisão de escopo/simplificação. **Não decidido nesta branch.**
2. Confirmar os modelos exatos e a disponibilidade dos componentes.
3. Confirmar pinagem, tensões, endereços I²C e alimentação após datasheets e módulos reais.
4. Definir o pluviômetro e o fator de conversão para `rain_mm`.
5. Definir o procedimento de calibração/interpretação do MQ-135.
6. Definir unidade/conversão de `luminosity_pct`.

## Estado de evidência

- **Projetado:** componentes, funções e relações descritos na arquitetura e nos requisitos.
- **Implementado em software:** campos de telemetria, estados, renderizadores e interfaces genéricas.
- **Simulado:** testes com fixtures, drivers fake e displays fake.
- **Validado em software:** contrato, validação de payload e separação estrutural testados localmente.
- **Pendente de hardware:** disponibilidade, montagem, alimentação, pinagem, endereços, leituras, calibração e operação física.
- **Validado fisicamente:** nenhum item nesta versão.
