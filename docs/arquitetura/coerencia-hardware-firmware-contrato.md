# Coerência entre hardware, firmware e contrato

**Classificação:** BASELINE APROVADA; VALIDADO EM SOFTWARE para estrutura/contrato; PENDENTE DE HARDWARE para integração física.  
**Referência:** ADR-002.

## Matriz de grandezas

| Campo | Fonte física aprovada | Semântica | Estado |
|---|---|---|---|
| `temperature_c` | DHT22 | °C | driver/teste físico pendentes |
| `humidity_pct` | DHT22 | umidade relativa % | driver/teste físico pendentes |
| `pressure_hpa` | BMP280 | hPa após conversão validada | driver/teste físico pendentes |
| `air_quality_raw` | MQ-135 | leitura bruta/experimental; não ppm | ADC/condicionamento/calibração pendentes |
| `luminosity_pct` | LDR | luminosidade relativa após conversão documentada | circuito/teste pendentes |
| `rain_mm` | sem fonte quantitativa calibrada nesta etapa | não publicar mm sem método/fator validados | compatibilidade contratual sob revisão |
| `timestamp` | NTP + relógio do sistema | ISO-8601; política temporal do projeto | integração no ESP32 pendente |
| `quality.*` | validação de cada aquisição | ok/suspect/invalid/error | estrutura parcialmente validada em software |

## Firmware

A estrutura existente de drivers, services, tasks e models continua aproveitável. A implementação concreta deve:

- criar/adaptar drivers para DHT22, BMP280, MQ-135, LDR e módulo de chuva;
- renderizar uma única OLED;
- remover dependências funcionais de TCA9548A, DS3231, BME280 adicional e segunda tela;
- manter API meteorológica externa desacoplada e complementar;
- usar NTP como sincronização temporal principal;
- não bloquear aquisição/telemetria por falha da OLED ou da API externa.

## Contrato

O schema v1.0 continua sendo a fronteira vigente enquanto a transição é executada. Não alterar silenciosamente o significado de `rain_mm`. Até existir pluviometria quantitativa defensável, o firmware deve representar ausência/invalidade conforme as regras do contrato, em vez de fabricar milímetros a partir do sensor de chuva.

## Dependências físicas

Ainda dependem do hardware recebido:

- GPIOs definitivos;
- endereços I²C;
- níveis de alimentação;
- condicionamento analógico;
- drivers concretos;
- calibração;
- comportamento offline;
- integração MQTT no dispositivo;
- testes de bancada e de campo.
