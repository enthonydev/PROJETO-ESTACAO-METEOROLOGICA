# Firmware

Firmware MicroPython do ESP32.

## Organização prevista
- `src/drivers/`: drivers de hardware.
- `src/services/`: conectividade, tempo, sensores e serviços externos.
- `src/displays/`: apresentação das duas telas.
- `src/tasks/`: ciclos independentes de execução.
- `src/models/`: estruturas de dados internas.
- `tests/`: testes aplicáveis ao firmware.

Não incluir credenciais reais. A pinagem deve seguir a documentação validada em `hardware/`.
