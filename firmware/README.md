# Firmware

Firmware MicroPython do ESP32. A pinagem deve seguir a documentação validada em `hardware/`.

## Firmware Arduino N2 (preparado, não validado fisicamente)

- `arduino/Estacao_Meteorologica_DEV_1_1/`: versão funcional aprovada na montagem atual, sem rede.
- `arduino/Estacao_Integrada_N2/`: firmware experimental, com perfis Wi-Fi 2,4 GHz, seleção por comando serial, MQTT, NTP, OLED e sensores existentes.
- `local_config.example.h`: copiar para `local_config.h` na máquina local, editar SSIDs/senhas e IP do broker; esse arquivo é ignorado pelo Git.
- BMP280 ou BME280 selecionado após confirmação física; MQ135 opcional apenas com alimentação/ADC seguros; LDR percentual não liberado até ADC1/calibração.
- Consulte `../docs/integracao/ensaio-wifi-mqtt-n2.md`.

**Status:** código novo aguardando compilação, medição elétrica e testes físicos. Não substituir o firmware validado sem rollback disponível.

---
