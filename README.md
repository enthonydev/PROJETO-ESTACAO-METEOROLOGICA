## Preparação da entrega N2 — 13 e 16 de novembro de 2026

**Situação:** infraestrutura de software pronta para ensaios; **estresse Wi-Fi e integração real ESP32 → MQTT → PostgreSQL → dashboard ainda precisam de execução presencial**. O roteiro acadêmico e as orientações para o vídeo ainda serão fornecidos pela equipe.

- [Plano de fechamento com checklist verificável](docs/academico/n2/plano-fechamento-13-16-novembro.md)
- [Roteiro de integração Wi-Fi/MQTT (casa, UNIP e terceira rede)](docs/integracao/ensaio-wifi-mqtt-n2.md)
- [Firmware experimental Arduino N2](firmware/arduino/Estacao_Integrada_N2/Estacao_Integrada_N2.ino)
- [Exemplo de configuração local, sem senhas](firmware/arduino/Estacao_Integrada_N2/local_config.example.h)
- [Ambiente Docker opcional de PostgreSQL/Mosquitto](deploy/local/docker-compose.yml)
- [Verificador de leitura real via API](scripts/check_live_station.py)

**Atenção:** o firmware que efetivamente foi validado em hardware é o **DEV 1.1**. A versão N2 acrescenta suporte a Wi-Fi, MQTT, NTP e integração futura com **BMP280 OU BME280** e MQ-135, mas essas funções novas **não foram compiladas nem validadas na placa**. Configurações reais de rede devem ficar em `local_config.h`, protegido por `.gitignore`. Não conectar novos sensores sem inspeção da tensão, pinos e limites de GPIO.

### O que está pronto

Backend FastAPI, schema v1.0, worker MQTT, PostgreSQL e dashboard Clima têm código e testes automatizados; o CI havia validado o fluxo com **publisher sintético**. A bancada confirmou DHT22, OLED, LDR digital e chuva digital. Para a entrega final precisamos juntar essas partes com **leituras físicas reais em Wi-Fi**, validar falhas/reconexões, revisar o cabeamento e produzir evidências e vídeo exigidos pelo professor.

---

## Interface Clima iOS (atualização)

A interface visual aprovada anteriormente foi recuperada do protótipo `preview_weather_ultra_interativo.html` e integrada ao backend existente, preservando animações, ambiente dinâmico, cards e gráfico interativo.

- `http://127.0.0.1:8000/dashboard/` abre a nova interface.
- `http://127.0.0.1:8000/dashboard/weather.html?station=estacao-esp32-real` acessa diretamente a estação física.
- `http://127.0.0.1:8000/dashboard/index.html` preserva a interface antiga somente como legado.
- A UI **não inventa** valores de sensores ausentes nem previsões horárias. Com ponte serial ativa, mostra temperatura e umidade reais e seus históricos.
- O ambiente dinâmico é visual, não substitui dados meteorológicos externos.
- Atualização automática a cada 10 s, por consultas REST locais; não exige nova dependência de frontend.

Para instalar/executar o backend e a ponte serial, consulte [o ensaio USB](docs/integracao/ensaio-serial-dev-1.1.md). O usuário que já iniciou a versão anterior deve parar o Uvicorn com Ctrl+C, baixar a `main` atualizada e iniciar novamente. Não há novo pacote Python para instalar.

---


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
| Telemetria | MQTT sobre Wi-Fi | Broker e consumidor validados em software; ESP32 ainda pendente |
| Contrato de dados | JSON v1.0 | Validado em software |
| Backend | Python + FastAPI | API de consulta e processamento MQTT implementados; broker/ESP32 reais pendentes |
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

## Atualização física — DEV 1.1 (01/11/2026)

**Situação confirmada em bancada:** ESP32 com firmware **Arduino/C++**, OLED SSD1306, DHT22, detecção digital de água e LDR digital funcionando simultaneamente. As leituras de chuva foram validadas nos dois estados (seco/molhado), assim como a alternância claro/escuro. O GPIO17 possui diagnóstico serial periódico de 5 segundos.

**Diferença em relação à arquitetura-alvo:** a N1 descrevia MicroPython + Wi-Fi/MQTT. A implementação física atual, testada, é Arduino/C++ via USB serial. Não foi demonstrada ainda comunicação ESP32 → MQTT ou integração física ponta a ponta com o backend; a solução USB serial é uma ponte **experimental para desenvolvimento**, sem alterar o contrato de telemetria v1.0.

- [Registro real de conexões e ensaios](hardware/registro-montagem-dev-1.1.md)
- [Firmware Arduino DEV 1.1](firmware/arduino/Estacao_Meteorologica_DEV_1_1/Estacao_Meteorologica_DEV_1_1.ino)
- [Execução do dashboard com o ESP32 pela USB](docs/integracao/ensaio-serial-dev-1.1.md)

### Ver a interface com medições reais (teste local)

No PowerShell, na raiz do repositório, instale as dependências:

```powershell
python -m pip install -r backend/requirements.txt
python -m pip install pyserial
```

Terminal 1:

```powershell
$env:PYTHONPATH="backend"
$env:ENABLE_HTTP_INGESTION="true"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Terminal 2, com o Monitor Serial do Arduino IDE fechado:

```powershell
python tools/serial_bridge.py --port COM7
```

Acesse **http://127.0.0.1:8000/dashboard/?station=estacao-esp32-real**.

O banco PostgreSQL **não é obrigatório para esse teste local**: o FastAPI já suporta armazenamento temporário em memória, que se perde quando reiniciado. PostgreSQL continua previsto para persistência e MQTT. Não abra o endpoint de ingestão sem autenticação na rede.

**Limitações honestas:** a interface recebe temperatura e umidade numéricas reais. Os estados digitais da chuva e da luz são exibidos no terminal da ponte e na OLED, mas o contrato atual não possui campos próprios para essas classificações. Portanto `rain_mm` e `luminosity_pct` permanecem `null`, assim como pressão e qualidade do ar ainda não conectadas. Não mostrar 0 mm, 0% ou dados fictícios como reais.

**Riscos e pendências:** houve um jumper solto e mau contato no furo E30 da protoboard; LDR usa GPIO5 (strapping); BMP280 permanece sem pinos soldados; MQ-135 de 5V não foi conectado por falta de espaço/cabos e demanda proteção de entrada. Teste real USB → API → dashboard ainda **pendente de execução com o hardware do usuário**.

---

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
- teste lógico MQTT → repositório → API REST;
- teste de integração com broker Mosquitto real → worker → PostgreSQL → API REST;
- validação de PostgreSQL 16 em runtime no CI;
- auditoria pré-hardware da N2 com correções de segurança e coerência operacional.

As evidências da N1 comprovam o estado documental e o comportamento validado em software. Elas não representam validação física da estação.

Permanecem para a N2 e etapas seguintes:

- publicação MQTT real pelo ESP32 em ambiente integrado;
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
- [Auditoria técnica da N2 — estado pré-hardware](docs/academico/n2/auditoria-software-pre-hardware.md)
- [Matriz de rastreabilidade da N2](docs/requisitos/matriz-rastreabilidade-n2.md)
- [Fechamento do software pré-hardware](docs/academico/n2/fechamento-software-pre-hardware.md)
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
