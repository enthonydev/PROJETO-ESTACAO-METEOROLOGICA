# Mapa conceitual de interconexões

**Classificação:** DIAGRAMA / MAPA CONCEITUAL  
**Não representa montagem validada, pinout definitivo ou validação elétrica.**

```text
                         ┌──────────────────────┐
                         │ ESP32 DevKit V1      │
                         │ MicroPython / Wi-Fi  │
                         └──────────┬───────────┘
                                    │
                              I²C / TBD
                                    │
                         ┌──────────▼───────────┐
                         │ TCA9548A              │
                         │ endereço: TBD         │
                         └──────┬─────────┬──────┘
                                │ CH0     │ CH1
                         ┌──────▼───┐ ┌──▼────────┐
                         │ OLED #1  │ │ OLED #2   │
                         │ Meteo    │ │ Relógio   │
                         │ SH1106   │ │ SH1106    │
                         └──────────┘ └───────────┘

                         I²C / TBD (a confirmar)
                              ┌──────┴──────┐
                         ┌────▼─────┐ ┌────▼─────┐
                         │ BME280   │ │ DS3231   │
                         │ local    │ │ RTC      │
                         └──────────┘ └──────────┘

       GPIO/ADC / TBD
       ┌──────────────┬──────────────┬──────────────┐
       ▼              ▼              ▼              ▼
    DHT22          BMP280         MQ-135          LDR       Pluviômetro
   (TBD)           (TBD)          ADC/TBD        ADC/TBD    pulso/TBD
```

## Interconexões sustentadas pela arquitetura

- O ESP32 é o controlador do firmware e da conectividade Wi-Fi.
- O TCA9548A é o multiplexador conceitual dos dois OLEDs iguais.
- CH0 é destinado à tela meteorológica; CH1, à tela de relógio/calendário.
- BME280 fornece, conceitualmente, temperatura, umidade e pressão para a visualização local.
- DS3231 fornece, conceitualmente, referência temporal local quando a internet não estiver disponível.
- DHT22, BMP280, MQ-135, LDR e pluviômetro aparecem na baseline/requisitos, mas seus modelos e conexões exatas continuam pendentes.

## O que não está definido neste documento

- GPIOs e pinout.
- Endereços I²C efetivos.
- Tensões e níveis lógicos.
- Resistores de pull-up.
- Alimentação comum ou separada.
- Modelo exato dos módulos.
- Fator de conversão do pluviômetro.
- Calibração/interpretação do MQ-135.
- Decisão entre coexistência ou simplificação de BME280, DHT22 e BMP280.

**Status físico:** SEM EVIDÊNCIA FÍSICA. A montagem, o circuito e o funcionamento deste mapa ainda não foram executados.
