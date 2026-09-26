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

## Decisão pendente

A divergência entre **BME280** e **DHT22 + BMP280** permanece registrada como decisão conjunta pendente de Luan, Enthony e James em [`docs/arquitetura/decisao-pendente-sensores.md`](../docs/arquitetura/decisao-pendente-sensores.md). Nenhum componente foi excluído ou escolhido unilateralmente.

A documentação desta pasta não deve ser usada para afirmar montagem, pinagem validada, leitura real, calibração ou teste físico.
