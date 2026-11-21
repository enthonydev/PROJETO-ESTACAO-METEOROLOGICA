# Firmware da bancada em MicroPython

Entrada: `src/main.py`, função `run_station()`. Instalação na raiz pelo `MIGRAR_ESP32.ps1`.

Mantém DHT22 GPIO16, chuva GPIO17, LDR GPIO5, I2C SDA21/SCL22 e OLED 0x3C. Pressão explicitamente DEMO, sem leitura do módulo 280. Wi-Fi roda de forma cooperativa: timeout, rotação de perfis e reconexão não interrompem os sensores. Ctrl+C interrompe o loop e devolve o REPL USB.

Consulte [o guia completo](../docs/integracao/migracao-micropython-bancada.md). A validação automatizada usa periféricos simulados e não substitui o ensaio na placa.
