# Estação Meteorológica Inteligente com ESP32

Projeto acadêmico desenvolvido na disciplina **Projeto e Desenvolvimento II**, do curso de Ciência da Computação.

O objetivo é desenvolver uma estação meteorológica inteligente de baixo custo para monitoramento ambiental urbano, integrando **ESP32**, sensores, firmware, comunicação em rede, backend em Python, banco de dados e dashboard web.

## Objetivo

Construir um sistema capaz de coletar, validar, transmitir, armazenar e apresentar dados ambientais, relacionando o projeto aos conceitos de **Internet das Coisas (IoT)** e **Cidades Inteligentes**.

## Arquitetura

Fluxo principal previsto:

```text
Sensores
   ↓
ESP32 / MicroPython
   ↓
Wi-Fi / MQTT
   ↓
Backend Python
   ↓
PostgreSQL
   ↓
API REST
   ↓
Dashboard Web
```

A estação também possui um subsistema local com dois displays OLED:

- **Display meteorológico:** informações ambientais locais e dados meteorológicos externos;
- **Display de relógio/calendário:** data e hora, com sincronização NTP e referência local por RTC DS3231.

Displays I²C de mesmo endereço são isolados por um multiplexador **TCA9548A**.

A baseline arquitetural detalhada está em [docs/arquitetura/arquitetura-sistema.md](docs/arquitetura/arquitetura-sistema.md).

## Componentes previstos

O projeto acadêmico contempla ESP32 e sensores para temperatura, umidade, pressão atmosférica, qualidade do ar, luminosidade e precipitação. A seleção e a validação final dos componentes, pinagem, alimentação e calibração são documentadas conforme os testes físicos avançam.

Componentes do subsistema local incluem ainda OLEDs SH1106, TCA9548A, BME280 e RTC DS3231.

> A presença de um componente nesta visão de projeto não significa que sua validação física já tenha sido concluída. Resultados e evidências são documentados separadamente.

## Software

A baseline técnica prevê:

- **MicroPython** no ESP32;
- **MQTT** para telemetria;
- **Python / FastAPI** no backend;
- **PostgreSQL** para persistência;
- **API REST** para consumo dos dados;
- dashboard web responsivo;
- versionamento do contrato de telemetria;
- testes e validação progressivos.

## Estrutura do repositório

O repositório será estruturado progressivamente conforme as sprints:

```text
docs/       documentação técnica e acadêmica
firmware/   firmware do ESP32
hardware/   diagramas, pinout, BOM e materiais de hardware
backend/    backend e API
frontend/   dashboard web
database/   modelagem, migrations e scripts de banco
scripts/    utilitários do projeto
```

Diretórios são adicionados quando passam a possuir artefatos reais; não são mantidas pastas vazias apenas para representar a arquitetura futura.

## Desenvolvimento

O trabalho é dividido em sprints e frentes paralelas de:

- hardware e validação física;
- software e arquitetura;
- produto, documentação e integração.

Alterações são desenvolvidas em branches próprias, revisadas por Pull Request e integradas à `main` somente após validação.

## Entregas acadêmicas

A documentação acompanha as entregas **N1** e **N2** da disciplina. O README será atualizado após o fechamento de cada marco para refletir somente funcionalidades e evidências efetivamente concluídas.

## Referências

A fundamentação acadêmica completa, com as referências efetivamente citadas no relatório, será mantida na documentação da N1 e atualizada na N2. Entre as referências técnicas e bibliográficas previstas no roteiro acadêmico estão:

- ALENCAR FILHO, Edgard. *Iniciação à Lógica Matemática*. Nobel, 2008.
- IDOETA, Ivan Valeije; CAPUANO, Francisco Gabriel. *Elementos de Eletrônica Digital*. 42. ed. Érica, 2019.
- KOLBAN, Neil. *Kolban's Book on ESP32*. Leanpub, 2018.
- LOURENÇO, Antonio Carlos de; CRUZ, Eduardo Cesar Alves; FERREIRA, Sabrina. *Circuitos Digitais*. 9. ed. Érica.
- MENEZES, Nilo Ney Coutinho. *Introdução à Programação com Python*. Novatec, 2019.
- OLIVEIRA, Sérgio de. *Internet das Coisas com ESP8266, ESP32 e Raspberry Pi*. Novatec, 2017.
- WINTERLE, Paulo. *Vetores e Geometria Analítica*. 2. ed. Pearson, 2014.

Datasheets, documentação oficial de bibliotecas, protocolos e demais fontes técnicas utilizadas serão registradas conforme forem efetivamente empregadas, evitando referências não utilizadas no trabalho final.

## Licença e segurança

O projeto é distribuído sob a **MIT License**. Orientações para relato responsável de vulnerabilidades e exposição acidental de credenciais estão em [SECURITY.md](SECURITY.md).

---

**Status:** desenvolvimento acadêmico em andamento. A documentação deste README representa a baseline atual e será revisada após a conclusão da N1.
