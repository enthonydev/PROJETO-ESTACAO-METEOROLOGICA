<div align="center">

# 🌦️ Estação Meteorológica Inteligente com ESP32

**Projeto acadêmico de monitoramento ambiental com ESP32, telemetria MQTT, backend Python e visualização web.**

![ESP32](https://img.shields.io/badge/ESP32-MicroPython-000000?style=for-the-badge&logo=espressif&logoColor=white)
![Python](https://img.shields.io/badge/Python-FastAPI-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Persistência-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-Telemetria-660066?style=for-the-badge&logo=mqtt&logoColor=white)

**N1 · Sprints 1–4 consolidadas**

</div>

---

## 📌 Sobre o projeto

A **Estação Meteorológica Inteligente com ESP32** é um projeto acadêmico voltado à aquisição, transmissão, armazenamento e visualização de dados ambientais.

A solução foi projetada para integrar sensores ao ESP32, transmitir telemetria via MQTT, processar e validar os dados em um backend Python, armazenar histórico em PostgreSQL e disponibilizar as informações por API REST e dashboard web.

Além da interface web, a arquitetura prevê duas telas OLED locais para informações meteorológicas e relógio/calendário.

## 🏗️ Arquitetura

```text
Sensores
   ↓
ESP32 / MicroPython
   ↓
Wi-Fi
   ↓
MQTT
   ↓
Backend / FastAPI
   ↓
PostgreSQL
   ↓
API REST
   ↓
Dashboard Web
```

O **MQTT** é o caminho principal projetado para a telemetria. A **API REST** atende às consultas do dashboard e não substitui a ingestão MQTT.

A arquitetura completa está documentada em [`docs/arquitetura/arquitetura-sistema.md`](docs/arquitetura/arquitetura-sistema.md).

## 🧰 Stack e componentes

| Camada | Tecnologia / componente | Situação |
|---|---|---|
| Microcontrolador | ESP32 DevKit V1 | Projetado |
| Firmware | MicroPython | Estrutura implementada |
| Telemetria | MQTT sobre Wi-Fi | Contrato definido |
| Contrato de dados | JSON v1.0 | Validado em software |
| Backend | Python + FastAPI | Implementado parcialmente |
| Persistência | PostgreSQL | Modelo e migration disponíveis |
| API | REST | Parcialmente implementada |
| Dashboard | Web responsivo | Projetado |
| Displays locais | 2× OLED SH1106 | Projetado |
| Sensores auxiliares | BME280 + DS3231 | Projetado |
| Multiplexador I²C | TCA9548A | Projetado |
| Integração física | ESP32 + sensores + displays | Bloqueada até montagem |

> **Importante:** “projetado” ou “implementado em software” não significa validação física. O projeto mantém essa distinção em toda a documentação.

## 🌡️ Dados ambientais previstos

O MVP contempla:

- temperatura;
- umidade;
- pressão atmosférica;
- indicador de qualidade do ar;
- luminosidade;
- precipitação.

Cada amostra deve possuir identificação da estação, timestamp e informação de qualidade das medições.

## 🖥️ Interfaces locais

A arquitetura prevê duas telas OLED **SH1106 128×64** independentes, utilizando o multiplexador **TCA9548A**:

**Display meteorológico**
- dados meteorológicos externos;
- temperatura local;
- umidade local;
- pressão atmosférica.

**Display de relógio**
- hora;
- data;
- dia da semana;
- sincronização por NTP;
- referência local pelo DS3231 quando necessário.

A camada de apresentação recebe dados processados pelos serviços do firmware e não consulta diretamente sensores, APIs ou NTP.

## 📡 Contrato de telemetria

O contrato atual está na versão **1.0**.

Tópico MQTT projetado:

```text
estacao/<station_id>/telemetry
```

Estrutura principal:

```text
schema_version
station_id
timestamp
location
measurements
quality
```

O contrato completo está em [`docs/contratos/telemetria-v1.0.json`](docs/contratos/telemetria-v1.0.json).

## 🚀 Estado atual

As **Sprints 1 a 4** estão consolidadas na `main`.

### ✅ Disponível no repositório

- requisitos funcionais e não funcionais;
- stakeholders e fronteiras de escopo;
- casos de uso;
- matriz de rastreabilidade;
- arquitetura do sistema;
- contrato de telemetria v1.0;
- backend FastAPI;
- endpoint `GET /health`;
- endpoint `POST /api/v1/telemetry/validate`;
- fixtures de telemetria válida, parcial e inválida;
- testes automatizados do backend;
- skeleton estrutural do firmware;
- serviços, estados, tasks, interfaces e renderizadores;
- testes estruturais de firmware com dependências simuladas;
- DER inicial;
- migration SQL para PostgreSQL;
- validações automatizadas no CI;
- relatório acadêmico consolidado da N1;
- auditorias de coerência técnica e acadêmica.

### ⏳ Pendente ou bloqueado

- ingestão MQTT real;
- persistência PostgreSQL em runtime;
- endpoints REST de consulta;
- dashboard funcional;
- drivers físicos;
- pinagem definitiva;
- montagem do hardware;
- calibração dos sensores;
- sensores e displays reais;
- integração ponta a ponta;
- testes de bancada e de campo.

> A evidência atual comprova comportamento e organização de **software**. Ela não comprova uma estação física integrada.

## 🧪 Validação

A base atual possui validações automatizadas para backend, contrato e estrutura do firmware.

O CI verifica os artefatos aplicáveis antes da integração das alterações na `main`.

As validações físicas serão registradas somente quando houver montagem e evidência reproduzível de bancada ou campo.

## 📚 Documentação da N1

Os principais documentos consolidados são:

- [Relatório acadêmico da N1](docs/academico/n1/relatorio-n1.md)
- [Insumos técnicos para consolidação](docs/academico/n1/insumos-tecnicos-consolidacao.md)
- [Arquitetura do sistema](docs/arquitetura/arquitetura-sistema.md)
- [Contrato de telemetria v1.0](docs/contratos/telemetria-v1.0.json)
- [Guia de contribuição](CONTRIBUTING.md)

## 🔀 Desenvolvimento e governança

O desenvolvimento ocorre em branches próprias. Cada alteração deve passar por **Pull Request** antes de chegar à `main`.

Antes de iniciar uma task, consulte o [`CONTRIBUTING.md`](CONTRIBUTING.md).

As entregas preservam a distinção entre:

```text
Projetado
   ↓
Implementado
   ↓
Simulado / Validado em software
   ↓
Validado fisicamente
```

Uma etapa não é promovida automaticamente para a seguinte. **Evidência de software não substitui validação física.**

---

<div align="center">

### 🎓 Projeto e Desenvolvimento II · Ciência da Computação

**Estação Meteorológica Inteligente com ESP32**

</div>
