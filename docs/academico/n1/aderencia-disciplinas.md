# Aderência às disciplinas acadêmicas

## 1. Objetivo e princípio

Este documento atende à task J-S3-04 da Sprint 3. As relações abaixo conectam o projeto a áreas acadêmicas somente quando há artefato, requisito ou teste correspondente no repositório. Uma relação indica aplicação técnica no projeto; não afirma que a disciplina foi validada por um resultado físico.

## 2. Relações justificadas

| Área ou disciplina | Aplicação no projeto | Artefatos e evidências | Estado |
|---|---|---|---|
| Engenharia de Software | Requisitos, casos de uso, metodologia incremental, branches, PRs, Gates, matriz de rastreabilidade e distinção entre evidência e pendência. | `docs/requisitos/`, `docs/academico/n1/metodologia-desenvolvimento.md`, matriz atualizada e governança Git. | Documentado e aplicado no processo |
| Engenharia de Requisitos | Identificação de RF/RNF, critérios de aceite, dependências, fronteiras de escopo e rastreabilidade até implementação e teste. | `requisitos-funcionais.md`, `requisitos-nao-funcionais.md`, `casos-de-uso.md` e `matriz-rastreabilidade-n1.md`. | Documentado; rastreabilidade em evolução |
| Sistemas Embarcados | Separação entre modelos, serviços, tarefas, displays e interfaces de drivers para ESP32/MicroPython. | `firmware/src/`, `firmware/tests/test_structure.py` e arquitetura. | Skeleton implementado e validado em software; hardware pendente |
| Internet das Coisas e Redes | Telemetria por MQTT, tópico versionado, Wi-Fi, broker, publicação/assinatura e desacoplamento entre estação e backend. | Contratos, arquitetura e fundamentação teórica. | Projetado; publicação MQTT real pendente |
| Programação e Desenvolvimento Web | API FastAPI, validação de payload, códigos HTTP e separação entre backend, API e futuro dashboard. | `backend/app/main.py`, schemas, serviços e testes de API. | Backend parcial validado em software; frontend pendente |
| Banco de Dados | Modelo relacional com estações, medições e qualidade por métrica; chaves, restrições, timestamps UTC e índice de série temporal. | DER e `database/migrations/001_schema_inicial.sql`. | Modelo/migration implementados; execução PostgreSQL pendente |
| Testes de Software e Qualidade | Testes de healthcheck, schema, payload parcial/inválido, isolamento de falhas, renderização e conversão temporal. | `backend/tests/`, `firmware/tests/` e CI. | Validado em software e simulação controlada |
| Sistemas Digitais e Eletrônica | Interfaces I2C, GPIO, ADC, displays OLED, TCA9548A, DS3231 e sensores são tratados como componentes da arquitetura. | Arquitetura e skeleton de interfaces. | Projetado; pinagem e validação de bancada bloqueadas |
| Instrumentação e Metrologia | Necessidade de calibração, referência, controle de qualidade, rastreabilidade, incerteza e distinção entre valor bruto e valor interpretado. | Fundamentação, contrato de qualidade e matriz. | Requisito metodológico; calibração física pendente |
| Matemática e Lógica | Estados de qualidade `ok`, `suspect`, `invalid` e `error`, regras de rejeição, valores nulos e interpretação condicional de falhas. | Schema, serviço de validação e testes. | Parcialmente implementado e validado em software |
| Geometria Analítica e Visualização Espacial | Latitude/longitude no contrato e no modelo de dados, com previsão de mapa no dashboard. | Schema, DER e arquitetura do dashboard. | Projetado; coordenadas reais e mapa ainda pendentes |
| Gestão de Projetos e Métodos Ágeis | Sprints, tasks, Gates, dependências, revisão por PR e integração centralizada. | Cronograma, metodologia e histórico de PRs. | Documentado e aplicado |

## 3. Limites das relações

A relação com Sistemas Digitais, Eletrônica, Instrumentação e Geometria Analítica não significa que os circuitos, sensores, coordenadas ou calibrações tenham sido validados. Nesta Sprint, essas áreas possuem aplicação projetada ou requisito metodológico, enquanto a evidência física permanece bloqueada.

A relação com Banco de Dados não significa que a persistência tenha sido executada em PostgreSQL. A migration e o DER estão versionados, mas a execução do banco, as consultas de histórico e os testes de integridade em ambiente persistente ainda não estão documentados como resultado desta entrega.

A relação com IoT e Redes não significa que exista uma transmissão MQTT comprovada. O protocolo e o tópico estão definidos na arquitetura e no contrato; broker, autenticação, reconexão, QoS operacional e disponibilidade devem ser testados quando a integração existir.

## 4. Síntese para a N1

O projeto integra conhecimentos de engenharia de software, sistemas embarcados, redes, desenvolvimento web, banco de dados, testes, instrumentação e visualização. A integração é demonstrada por requisitos, arquitetura, código, fixtures, testes de software, SQL e governança. A parte física é apresentada como projeto ou pendência enquanto não houver montagem, pinagem, calibração e evidência de bancada.

## 5. Referências internas

[1]: ../../requisitos/matriz-rastreabilidade-n1.md "Matriz de rastreabilidade da N1"
[2]: metodologia-desenvolvimento.md "Metodologia de desenvolvimento da N1"
[3]: arquitetura-dados-hardware.md "Arquitetura, dados e hardware da N1"
[4]: prototipo-e-testes.md "Protótipo e casos de teste da N1"
[5]: ../../arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
[6]: ../../contratos/contratos-integracao.md "Contratos de integração"
