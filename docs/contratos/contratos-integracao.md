# Contrato de integração da telemetria

## Escopo

Este documento define a mensagem de telemetria produzida pelo ESP32 e consumida pelo backend. O schema normativo está em [`telemetria-v1.0.json`](telemetria-v1.0.json).

## Transporte

A telemetria deve ser publicada por MQTT sobre Wi-Fi no tópico:

```text
estacao/<station_id>/telemetry
```

O segmento `<station_id>` deve corresponder ao campo `station_id` do payload. O backend não deve associar uma estação desconhecida silenciosamente.

## Versionamento

A versão atual do contrato é `1.0` e deve aparecer no campo `schema_version`. Mudanças incompatíveis exigem nova versão, estratégia de compatibilidade e ADR antes da implementação.

Uma mensagem incompatível não deve ser corrigida silenciosamente. O backend deve rejeitá-la e registrar a falha de ingestão.

## Campos

O payload contém identificação da estação, timestamp, localização, medições e qualidade individual das métricas. Os nomes e unidades do schema são:

| Campo | Unidade ou semântica |
| --- | --- |
| `temperature_c` | temperatura em graus Celsius, quando disponível |
| `humidity_pct` | umidade relativa em percentual, quando disponível |
| `pressure_hpa` | pressão atmosférica em hPa, quando disponível |
| `air_quality_raw` | leitura bruta do indicador de qualidade do ar |
| `luminosity_pct` | luminosidade relativa em percentual, quando disponível |
| `rain_mm` | precipitação em milímetros, quando houver conversão documentada |

Valores podem ser `null` quando a leitura não estiver disponível. O estado correspondente deve ser registrado como `error` ou outro estado aplicável. O contrato não autoriza inventar valores, faixas físicas, calibrações ou conversões.

## Estados de qualidade

- `ok`: leitura disponível e aceita pela validação vigente;
- `suspect`: leitura disponível, mas requer tratamento ou análise adicional;
- `invalid`: leitura rejeitada pela regra de validade aplicável;
- `error`: não foi possível obter a leitura.

O estado de qualidade não substitui a validação do backend. A mensagem também deve passar por validação de schema, timestamp, estação e integridade.

## Exemplos

Os exemplos estão em [`examples/`](examples/). Eles são exemplos de contrato, não evidências de sensor físico nem definição de calibração.

- `telemetry-v1.0-valid.json`: todas as métricas disponíveis;
- `telemetry-v1.0-partial.json`: falha parcial representada sem substituir o valor ausente.
