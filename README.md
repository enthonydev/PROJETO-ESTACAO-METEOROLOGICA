# Estação Meteorológica Inteligente com ESP32

Projeto acadêmico de uma estação meteorológica urbana baseada em ESP32, sensores ambientais, telemetria MQTT, backend Python, PostgreSQL e dashboard web público.

## Fluxo principal

```text
Sensores → ESP32/MicroPython → Wi-Fi → MQTT → Backend/FastAPI → PostgreSQL → API REST → Dashboard
```

O MQTT é o caminho principal da telemetria. A API REST atende as consultas do dashboard e não substitui a ingestão MQTT.

## Baseline técnica

- Firmware: MicroPython no ESP32 DevKit V1.
- Transporte de telemetria: MQTT sobre Wi-Fi.
- Contrato: JSON versionado, atualmente na versão `1.0`.
- Backend: Python com FastAPI.
- Persistência: PostgreSQL.
- Interface: dashboard web responsivo, desacoplado do banco.

A baseline detalhada, as pendências e os limites de mudança estão documentados em [`docs/arquitetura/arquitetura-sistema.md`](docs/arquitetura/arquitetura-sistema.md). O contrato de telemetria está em [`docs/contratos/telemetria-v1.0.json`](docs/contratos/telemetria-v1.0.json).

## Desenvolvimento

O desenvolvimento ocorre em branches próprias e cada alteração deve passar por Pull Request. Consulte [`CONTRIBUTING.md`](CONTRIBUTING.md) antes de iniciar uma task.

## Estado atual

O repositório está na etapa de especificação e baseline da Sprint 1. Ainda não há implementação de firmware, backend, banco ou frontend.
