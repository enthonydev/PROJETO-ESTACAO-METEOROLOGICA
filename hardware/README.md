# Hardware

Área de BOM, pinout, diagramas, simulação e validação física. Nesta versão, os artefatos preparatórios estão documentados, mas **não há montagem, leitura, calibração ou validação física realizada**.

## Estado atual

- **Projetado:** arquitetura, componentes previstos e mapa conceitual de interconexões.
- **Implementado em software:** interfaces genéricas de drivers, estados, serviços, tasks e renderizadores no firmware.
- **Simulado/validado em software:** fixtures, drivers fake, displays fake, contrato e testes estruturais existentes.
- **Pendente de hardware:** modelos reais, disponibilidade, datasheets aplicáveis, alimentação, GPIOs, endereços I²C, drivers concretos, leituras, calibração, montagem e testes de bancada/campo.
- **Validado fisicamente:** nenhum item.

## Artefatos

- [`bom.md`](bom.md): matriz de componentes, requisitos, interfaces, estados e pendências.
- [`pinout.md`](pinout.md): pinout preliminar; GPIOs, tensões e endereços permanecem TBD.
- [`diagrams/interconexoes.md`](diagrams/interconexoes.md): mapa conceitual, não montagem validada.
- [`plano-testes.md`](plano-testes.md): casos de teste preparados; resultados físicos estão como `NÃO EXECUTADO`.
- [`datasheets/`](datasheets/): reservado para datasheets oficiais dos modelos reais confirmados.
- [`evidencias/`](evidencias/): reservado para evidências futuras, sem evidência física disponível nesta versão.
- [`wokwi/`](wokwi/): reservado para simulação Wokwi; nenhum projeto Wokwi foi declarado como executado nesta versão.

## Baseline aprovada

O [`ADR-002`](../docs/arquitetura/adr/ADR-002-adequacao-arquitetura-fisica-orcamento.md) encerrou a decisão de baseline física: DHT22 para temperatura/umidade, BMP280 para pressão, MQ-135 bruto/experimental, LDR relativo, módulo de chuva experimental, uma OLED I²C 128x64 e ESP32 DevKit V1. BME280 adicional, DS3231, segunda OLED e TCA9548A foram removidos da baseline. O registro da decisão e suas limitações permanece em [`docs/arquitetura/decisao-pendente-sensores.md`](../docs/arquitetura/decisao-pendente-sensores.md).

A documentação desta pasta não deve ser usada para afirmar montagem, pinagem validada, leitura real, calibração ou teste físico.

## Integração física da N2 — pendências

- DHT22, OLED, detecção de chuva e LDR digital: leituras funcionais descritas em `registro-montagem-dev-1.1.md`.
- BMP280/BME280: identificar modelo real, soldar header corretamente, conferir alimentação e compartilhar SDA21/SCL22 se eletricamente compatível.
- MQ-135: verificar tensão/corrente do aquecedor (normalmente 5 V) e tensão analógica de saída; não alimentar com divisor ou resistor série para tentar regular. Se AO ultrapassar limite ADC, usar divisor de sinal e confirmar com multímetro.
- Usar GPIO ADC1 acessível para novas entradas analógicas, sem conflito com outros circuitos; nunca presumir que GPIO34/35 têm furos acessíveis na montagem atual.
- Nenhum sensor novo deve ser energizado antes de revisão física de ligação e polaridade.
- Plano de ensaios de Wi-Fi e integração em `../docs/academico/n2/plano-fechamento-13-16-novembro.md`.

---
