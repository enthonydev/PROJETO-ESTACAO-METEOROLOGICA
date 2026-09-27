# Wokwi — plano de simulação

**Estado:** NÃO EXECUTADO / SIMULAÇÃO NÃO CRIADA nesta versão.

O ADR-002 já definiu a baseline física: ESP32, DHT22, BMP280, MQ-135, LDR, módulo de chuva experimental e uma OLED I²C 128x64. Foram removidos da baseline o BME280 adicional, DS3231, segunda OLED e TCA9548A.

A simulação ainda não é criada porque os modelos comerciais exatos, GPIOs, níveis elétricos e endereços I²C dependem dos módulos que serão adquiridos. O objetivo é evitar uma representação aparentemente completa baseada em componentes ou ligações presumidos.

## Escopo permitido antes do hardware

- exercitar lógica do firmware com doubles/fixtures;
- documentar interfaces conceituais;
- testar estados e falhas de software;
- preparar o procedimento de bancada.

## Escopo após confirmação dos módulos

- ESP32 e periféricos que possuam representação adequada;
- DHT22 e BMP280;
- OLED única;
- sensores analógicos/digitais somente quando o modelo de simulação representar de forma útil o comportamento necessário;
- GPIOs coerentes com o pinout aprovado;
- registro explícito de qualquer diferença entre simulação e montagem real.

## Limitações

Wokwi será sempre evidência **SIMULADA**. Não comprova alimentação real, níveis elétricos do módulo comprado, endereço efetivo, estabilidade, calibração, leitura ambiental, desempenho da OLED ou teste de campo.

MQ-135 não deve ser apresentado em ppm sem calibração. LDR permanece leitura relativa até calibração. O módulo de chuva não sustenta `rain_mm` quantitativo sem método/fator validado.

Quando os anúncios/modelos adquiridos forem conhecidos, este diretório poderá receber o projeto e seu procedimento reproduzível.
