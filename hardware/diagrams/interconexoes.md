# Mapa conceitual de interconexões

**Classificação:** BASELINE APROVADA / CONEXÕES FÍSICAS A VALIDAR  
**Decisão arquitetural:** ADR-002.

```text
 DHT22 ───────── GPIO ───────┐
 BMP280 ───────── I²C ───────┤
 MQ-135 ───────── ADC ───────┤
 LDR ──────────── ADC ───────┼──> ESP32 DevKit V1
 Sensor de chuva ─ ADC/GPIO ─┤          │
 OLED 128x64 ───── I²C ──────┘          ├── Wi-Fi ── MQTT ── Backend
                                       ├── NTP
                                       └── API meteorológica externa
                                           (complementar)
```

## Responsabilidades

- DHT22: temperatura e umidade locais.
- BMP280: pressão atmosférica local.
- MQ-135: resposta bruta relacionada à qualidade do ar.
- LDR: luminosidade relativa.
- módulo de chuva: detecção/avaliação experimental; não representa pluviometria calibrada em mm.
- OLED: única interface embarcada local.
- NTP: referência temporal quando houver conectividade.
- API externa: informação complementar, sem substituir aquisição local.

## Removidos da arquitetura física

BME280 adicional, DS3231, TCA9548A e segunda OLED.

## Ainda não definido

GPIOs, tensões, níveis lógicos, endereços I²C, pull-ups, condicionamento do MQ-135, divisor do LDR e características elétricas do módulo de chuva dependem dos componentes reais e de validação de bancada.

**Status físico:** sem evidência física até a montagem.
