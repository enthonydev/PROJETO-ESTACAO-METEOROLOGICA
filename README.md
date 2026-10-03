<div align="center">

# Estação Meteorológica Inteligente com ESP32

**Projeto acadêmico de monitoramento ambiental com ESP32, telemetria MQTT, backend Python e visualização web.**

![ESP32](https://img.shields.io/badge/ESP32-MicroPython-000000?style=flat-square&logo=espressif&logoColor=white)
![Python](https://img.shields.io/badge/Python-FastAPI-3776AB?style=flat-square&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Persistência-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-Telemetria-660066?style=flat-square&logo=mqtt&logoColor=white)

N1 · Sprints 1–5 concluídas

</div>

---

## Sobre o projeto

A Estação Meteorológica Inteligente com ESP32 é um projeto acadêmico voltado à coleta, transmissão, armazenamento e visualização de dados ambientais.

A solução foi projetada para integrar sensores ao ESP32, transmitir telemetria via MQTT, processar e validar os dados em um backend Python, armazenar o histórico em PostgreSQL e disponibilizar as informações por API REST e dashboard web.

Além da interface web, a baseline física prevê uma OLED I²C 128x64 como interface local. A sincronização temporal usa NTP como referência principal, e a API meteorológica externa permanece apenas como fonte complementar.

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
| Telemetria | MQTT sobre Wi-Fi | Consumidor backend implementado; broker/ESP32 ainda pendentes |
| Contrato de dados | JSON v1.0 | Validado em software |
| Backend | Python + FastAPI | API de consulta implementada; ingestão MQTT pendente |
| Persistência | PostgreSQL | Repositório implementado e validado em runtime no CI |
| API | REST | Consultas do dashboard implementadas |
| Dashboard | HTML, CSS e JavaScript | Implementado e integrado à API REST; hardware não necessário |
| Sensores físicos | DHT22 + BMP280 + MQ-135 + LDR + chuva experimental | Baseline aprovada; validação física prevista para N2 |
| Display local | 1× OLED I²C 128x64 | Baseline aprovada; validação física prevista para N2 |
| Referência temporal | NTP | Projetado; validação no ESP32 prevista para N2 |

## Telemetria

O contrato atual está na versão `1.0`.

Tópico MQTT projetado:

```text
estacao/<station_id>/telemetry
```

O payload contempla identificação da estação, timestamp, localização, medições e estado de qualidade de cada métrica.

O contrato completo está em [`docs/contratos/telemetria-v1.0.json`](docs/contratos/telemetria-v1.0.json).

## Estado atual

A N1 foi concluída após cinco sprints de especificação, projeto técnico, implementação mínima, consolidação acadêmica e auditoria final.

Na Sprint 5, a equipe revisou a coerência entre requisitos, arquitetura, contrato de telemetria, firmware, backend, modelagem de dados, testes e documentação. A auditoria não identificou bloqueadores acadêmicos para a entrega da N1.

Já estão disponíveis no repositório:

- requisitos funcionais e não funcionais, casos de uso e matriz de rastreabilidade;
- arquitetura e contrato de telemetria v1.0;
- backend FastAPI com healthcheck, validação de telemetria, consultas de estação/histórico/resumo e ingestão HTTP de apoio ao desenvolvimento;
- fixtures e testes automatizados do backend;
- estrutura inicial do firmware com serviços, estados, tasks, interfaces e renderizadores;
- testes estruturais de firmware com dependências simuladas;
- DER e migration inicial para PostgreSQL;
- CI para validação do contrato, testes e compilação Python;
- relatório acadêmico consolidado da N1, insumos técnicos e auditorias de coerência;
- auditoria final da Sprint 5 da frente de software, arquitetura e integração técnica;
- dashboard web responsivo com histórico multi-métrica, estados operacionais, exportação CSV, cenários de demonstração e testes estáticos no CI;
- integração frontend/backend pela mesma aplicação FastAPI, com dados sintéticos em memória quando não há banco configurado;
- implementação de repositório PostgreSQL selecionada automaticamente quando `DATABASE_URL` estiver configurada;
- consumidor MQTT com validação de tópico, contrato e correspondência de `station_id`;
- teste ponta a ponta simulado MQTT → repositório → API REST;
- validação de PostgreSQL 16 em runtime no CI.

As evidências da N1 comprovam o estado documental e o comportamento validado em software. Elas não representam validação física da estação.

Permanecem para a N2 e etapas seguintes:

- ingestão MQTT real;
- conexão do consumidor MQTT a um broker de integração/produção;
- publicação MQTT real pelo ESP32;
- drivers e pinagem definitivos;
- confirmação dos modelos, níveis elétricos e endereços dos módulos adquiridos;
- montagem e calibração ou caracterização aplicável;
- validação física dos sensores e da OLED;
- integração ponta a ponta;
- testes de bancada, estabilidade e campo;
- execução dos testes físicos HW-T01 a HW-T19.

## N1

A primeira entrega acadêmica consolida problema, objetivos, requisitos, casos de uso, arquitetura, metodologia, modelagem de dados, protótipo de software, testes, resultados disponíveis, limitações e planejamento das validações físicas.

A N1 foi estruturada para não apresentar como concluído aquilo que ainda depende de hardware ou infraestrutura. Montagem, calibração, medições reais, integração física e testes de campo fazem parte da continuidade do projeto na N2.

## Documentação

- [Relatório acadêmico da N1](docs/academico/n1/relatorio-n1.md)
- [Auditoria da Sprint 5 — frente técnica](docs/academico/n1/auditoria-sprint-5-enthony.md)
- [Auditoria consolidada da N1](docs/academico/n1/auditoria-consolidacao-n1.md)
- [Insumos técnicos consolidados](docs/academico/n1/insumos-tecnicos-consolidacao.md)
- [Arquitetura do sistema](docs/arquitetura/arquitetura-sistema.md)
- [ADR-002 — adequação da arquitetura física](docs/arquitetura/adr/ADR-002-adequacao-arquitetura-fisica-orcamento.md)
- [Contrato de telemetria v1.0](docs/contratos/telemetria-v1.0.json)
- [Plano de testes de hardware](hardware/plano-testes.md)
- [Frontend e execução local](frontend/README.md)
- [Guia de contribuição](CONTRIBUTING.md)

## Desenvolvimento

O desenvolvimento ocorre em branches próprias e cada alteração deve passar por Pull Request antes de chegar à `main`.

Consulte o [`CONTRIBUTING.md`](CONTRIBUTING.md) antes de iniciar uma task.

O projeto diferencia itens projetados, implementados, simulados, validados em software e validados fisicamente. Evidência de software não substitui validação física.

---

<div align="center">

Projeto e Desenvolvimento II · Ciência da Computação · CC2P04

</div>
