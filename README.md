# Estação Meteorológica Inteligente com ESP32

Projeto acadêmico de uma estação meteorológica urbana baseada em ESP32, sensores ambientais, telemetria MQTT, backend Python, PostgreSQL e dashboard web público.

## Fluxo principal

```text
Sensores → ESP32/MicroPython → Wi-Fi → MQTT → Backend/FastAPI → PostgreSQL → API REST → Dashboard Web
```

O MQTT é o caminho principal projetado para a telemetria. A API REST atende às consultas do dashboard e não substitui a ingestão MQTT.

## Baseline técnica

- Firmware: MicroPython no ESP32 DevKit V1.
- Transporte de telemetria: MQTT sobre Wi-Fi.
- Contrato: JSON versionado, atualmente na versão `1.0`.
- Backend: Python com FastAPI.
- Persistência projetada: PostgreSQL.
- Interface projetada: dashboard web responsivo, desacoplado do banco.
- Interface local projetada: duas telas OLED SH1106, com BME280, DS3231 e TCA9548A.

A arquitetura detalhada está em [`docs/arquitetura/arquitetura-sistema.md`](docs/arquitetura/arquitetura-sistema.md), e o contrato de telemetria em [`docs/contratos/telemetria-v1.0.json`](docs/contratos/telemetria-v1.0.json).

## Estado atual

As Sprints 1 a 4 foram consolidadas na `main`. O projeto possui atualmente:

- requisitos funcionais e não funcionais, casos de uso e matriz de rastreabilidade;
- arquitetura e contrato de telemetria v1.0;
- backend FastAPI com `GET /health` e `POST /api/v1/telemetry/validate`;
- fixtures e testes automatizados do backend;
- skeleton estrutural de firmware com serviços, estados, tasks, interfaces e renderizadores;
- testes estruturais de firmware com dependências simuladas;
- DER e migration inicial para PostgreSQL;
- CI para validação do contrato, testes e compilação Python;
- relatório acadêmico consolidado da N1 e auditorias de coerência.

A evidência atual comprova comportamento e organização de **software**, não uma estação física integrada. Permanecem pendentes ou bloqueados, conforme a dependência: ingestão MQTT real, persistência PostgreSQL em runtime, endpoints REST de consulta, dashboard funcional, drivers físicos, pinagem, montagem, calibração, sensores e displays reais, integração ponta a ponta e testes de campo.

O relatório consolidado da N1 está em [`docs/academico/n1/relatorio-n1.md`](docs/academico/n1/relatorio-n1.md), e os limites técnicos atuais estão resumidos em [`docs/academico/n1/insumos-tecnicos-consolidacao.md`](docs/academico/n1/insumos-tecnicos-consolidacao.md).

## Desenvolvimento

O desenvolvimento ocorre em branches próprias e cada alteração deve passar por Pull Request. Consulte [`CONTRIBUTING.md`](CONTRIBUTING.md) antes de iniciar uma task.

Mudanças devem preservar a distinção entre itens projetados, implementados, simulados, validados em software, pendentes, bloqueados e fisicamente validados. Evidência de software não substitui validação física.
