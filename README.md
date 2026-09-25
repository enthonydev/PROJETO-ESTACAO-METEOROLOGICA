<div align="center">

# Estação Meteorológica Inteligente com ESP32

**Projeto acadêmico de monitoramento ambiental com ESP32, telemetria MQTT, backend Python e visualização web.**

![ESP32](https://img.shields.io/badge/ESP32-MicroPython-000000?style=flat-square&logo=espressif&logoColor=white)
![Python](https://img.shields.io/badge/Python-FastAPI-3776AB?style=flat-square&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Persistência-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-Telemetria-660066?style=flat-square&logo=mqtt&logoColor=white)

N1 · Sprints 1–4 consolidadas

</div>

---

## Sobre o projeto

A Estação Meteorológica Inteligente com ESP32 é um projeto acadêmico voltado à coleta, transmissão, armazenamento e visualização de dados ambientais.

A solução foi projetada para integrar sensores ao ESP32, transmitir telemetria via MQTT, processar e validar os dados em um backend Python, armazenar o histórico em PostgreSQL e disponibilizar as informações por API REST e dashboard web.

Além da interface web, a arquitetura prevê duas telas OLED locais para informações meteorológicas e relógio/calendário.

## Arquitetura

```text
Sensores → ESP32/MicroPython → Wi-Fi → MQTT → Backend/FastAPI → PostgreSQL → API REST → Dashboard Web
```

O MQTT é o caminho principal projetado para a telemetria. A API REST atende às consultas do dashboard e não substitui a ingestão MQTT.

A arquitetura completa está documentada em [`docs/arquitetura/arquitetura-sistema.md`](docs/arquitetura/arquitetura-sistema.md).

## Stack

| Camada | Tecnologia / componente | Situação atual |
| --- | --- | --- |
| Microcontrolador | ESP32 DevKit V1 | Projetado |
| Firmware | MicroPython | Estrutura implementada |
| Telemetria | MQTT sobre Wi-Fi | Contrato definido |
| Contrato de dados | JSON v1.0 | Validado em software |
| Backend | Python + FastAPI | Implementado parcialmente |
| Persistência | PostgreSQL | Modelo e migration disponíveis |
| API | REST | Parcialmente implementada |
| Dashboard | HTML, CSS e JavaScript | Projetado |
| Displays locais | 2× OLED SH1106 | Projetado |
| Sensores auxiliares | BME280 + DS3231 | Projetado |
| Multiplexador I²C | TCA9548A | Projetado |

## Telemetria

O contrato atual está na versão `1.0`.

Tópico MQTT projetado:

```text
estacao/<station_id>/telemetry
```

O payload contempla identificação da estação, timestamp, localização, medições e estado de qualidade de cada métrica.

O contrato completo está em [`docs/contratos/telemetria-v1.0.json`](docs/contratos/telemetria-v1.0.json).

## Estado atual

As Sprints 1 a 4 foram consolidadas na `main`.

Já estão disponíveis no repositório:

- requisitos funcionais e não funcionais, casos de uso e matriz de rastreabilidade;
- arquitetura e contrato de telemetria v1.0;
- backend FastAPI com `GET /health` e `POST /api/v1/telemetry/validate`;
- fixtures e testes automatizados do backend;
- estrutura inicial do firmware com serviços, estados, tasks, interfaces e renderizadores;
- testes estruturais de firmware com dependências simuladas;
- DER e migration inicial para PostgreSQL;
- CI para validação do contrato, testes e compilação Python;
- relatório acadêmico consolidado da N1 e auditorias de coerência.

Ainda dependem das próximas etapas ou de hardware:

- ingestão MQTT real;
- persistência PostgreSQL em runtime;
- endpoints REST de consulta;
- dashboard funcional;
- drivers e pinagem definitivos;
- montagem e calibração;
- sensores e displays reais;
- integração ponta a ponta;
- testes de bancada e de campo.

A evidência atual comprova comportamento e organização de software. Não representa validação física da estação.

## Documentação

- [Relatório acadêmico da N1](docs/academico/n1/relatorio-n1.md)
- [Insumos técnicos consolidados](docs/academico/n1/insumos-tecnicos-consolidacao.md)
- [Arquitetura do sistema](docs/arquitetura/arquitetura-sistema.md)
- [Contrato de telemetria v1.0](docs/contratos/telemetria-v1.0.json)
- [Guia de contribuição](CONTRIBUTING.md)

## Desenvolvimento

O desenvolvimento ocorre em branches próprias e cada alteração deve passar por Pull Request antes de chegar à `main`.

Consulte o [`CONTRIBUTING.md`](CONTRIBUTING.md) antes de iniciar uma task.

O projeto diferencia itens projetados, implementados, simulados, validados em software e validados fisicamente. Evidência de software não substitui validação física.

---

<div align="center">

Projeto e Desenvolvimento II · Ciência da Computação

</div>
