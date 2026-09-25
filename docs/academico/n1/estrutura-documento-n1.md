# Estrutura proposta do documento da N1

## 1. Objetivo e estado

Este documento atende à task J-S2-05 da Sprint 2. Ele propõe a organização do documento acadêmico da N1 a partir do Guia Mestre, do plano de sprints e dos artefatos já disponíveis no repositório.

**Estado:** estrutura proposta, não versão final. A liberação final depende da confirmação do roteiro do professor e do recebimento dos insumos de Enthony e Luan. Nenhuma seção pendente deve ser preenchida com resultados, referências, pinagem, calibração ou evidência inventados.

## 2. Estrutura proposta

### 2.1 Elementos iniciais

1. Capa e identificação da disciplina.
2. Resumo, se exigido pelo roteiro do professor.
3. Sumário.
4. Lista de figuras, tabelas e siglas, quando aplicável.

A necessidade e a ordem exatas desses elementos permanecem **TBD** até a confirmação do roteiro acadêmico.

### 2.2 Contextualização do problema

Esta seção deve apresentar o contexto de monitoramento ambiental urbano, o problema abordado, a justificativa do projeto, o objetivo geral e os objetivos específicos. O conteúdo inicial está em `docs/requisitos/contexto-escopo-objetivos.md`.

### 2.3 Stakeholders e escopo

Esta seção deve identificar os stakeholders, o MVP, o que está fora do MVP, as fronteiras do sistema e as dependências entre frentes. O conteúdo inicial está em `docs/requisitos/stakeholders-e-escopo.md`.

### 2.4 Requisitos e casos de uso

Esta seção deve apresentar requisitos funcionais, requisitos não funcionais, critérios de aceite, atores, casos de uso e a matriz de rastreabilidade. Os artefatos atuais são:

- `docs/requisitos/requisitos-funcionais.md`;
- `docs/requisitos/requisitos-nao-funcionais.md`;
- `docs/requisitos/casos-de-uso.md`;
- `docs/requisitos/matriz-rastreabilidade-n1.md`.

### 2.5 Metodologia e planejamento

Esta seção deve apresentar o processo de desenvolvimento, a organização em sprints, o fluxo de branches e Pull Requests, os critérios de revisão, o tratamento de dependências e a classificação das evidências. Os artefatos atuais são:

- `docs/academico/n1/metodologia-desenvolvimento.md`;
- `docs/academico/n1/cronograma-n1.md`.

### 2.6 Fundamentação teórica

Esta seção deve relacionar Smart Cities, monitoramento ambiental, IoT, ESP32, sensores, MQTT, backend, banco de dados, geolocalização, dashboard e disciplinas integradas ao problema do projeto. Cada afirmação deve possuir fonte confiável e verificável. A fundamentação está pendente de consolidação e revisão das fontes.

### 2.7 Arquitetura e decisões técnicas

Esta seção deve apresentar a arquitetura de hardware e software, o fluxo de dados, as responsabilidades dos componentes, o contrato de telemetria, as escolhas tecnológicas e as decisões arquiteturais. Devem ser usados os artefatos versionados em `docs/arquitetura/`, `docs/contratos/` e `docs/arquitetura/adr/`.

Decisões ainda não aprovadas devem ser identificadas como propostas. A seção não deve transformar a ADR-001, enquanto estiver com status proposto, em decisão definitivamente aprovada.

### 2.8 Modelagem de dados

Esta seção deve apresentar o modelo conceitual, lógico e físico no nível exigido pela N1, incluindo entidades, chaves, relacionamentos, integridade, timestamps e índice de série temporal. O DER e a migration de Enthony estão integrados na `main`; sua execução contra PostgreSQL e a persistência em runtime ainda não possuem evidência nesta etapa.

### 2.9 Protótipo e simulação

Esta seção deve registrar o protótipo, a simulação e os fixtures disponíveis. Cada evidência deve informar se é simulada, produzida por software ou física. A indisponibilidade de hardware não pode ser ocultada nem convertida em validação física.

### 2.10 Plano e casos de teste

Esta seção deve apresentar a estratégia de testes, os casos de teste, os requisitos relacionados, os resultados esperados, os resultados obtidos e as evidências. Testes ainda não executados devem permanecer como planejados ou pendentes.

### 2.11 Resultados e análise

Os resultados devem ser apresentados separadamente da interpretação. Não deve haver resultado nesta seção antes da execução correspondente. Limitações de hardware, software, calibração, infraestrutura e dados devem ser registradas junto às conclusões aplicáveis.

### 2.12 Conclusões e trabalhos futuros

As conclusões devem retornar aos objetivos e distinguir o que foi efetivamente demonstrado do que permaneceu pendente. Machine Learning, rede mesh, aplicativo mobile, energia solar obrigatória, caixa IP65 e alertas multicanal podem ser registrados como trabalhos futuros, conforme o Guia Mestre, sem ampliar o MVP.

### 2.13 Referências e apêndices

A versão final deve incluir referências no padrão solicitado pelo professor e apêndices técnicos, como contrato de telemetria, fixtures, diagramas, tabelas de rastreabilidade, casos de teste e evidências selecionadas.

## 3. Dependências para liberar a estrutura final

| Dependência | Impacto | Estado |
|---|---|---|
| Roteiro ou rubrica oficial do professor | Pode alterar a ordem, os títulos e a extensão das seções | BLOQUEADA até confirmação |
| Insumos de Enthony | Necessários para modelagem técnica, backend e resultados disponíveis | Backend, DER, migration, firmware estrutural e testes técnicos integrados na `main`; MQTT, persistência runtime e hardware continuam pendentes |
| Insumos de Luan | Necessários para hardware, pinout, protótipo e evidências físicas | Não localizados; BLOQUEADA a parte física |
| Fundamentação teórica revisada | Necessária para fechar a seção acadêmica | Em elaboração na J-S2-03 |
| Casos de teste e evidências | Necessários para resultados e análise | Parcialmente disponíveis; conclusão pendente |

## 4. Critério de aceite da task

A task será considerada aplicável nesta etapa quando a estrutura proposta estiver versionada, vinculada aos artefatos existentes e acompanhada das dependências que impedem a versão final. A estrutura não será apresentada como documento N1 concluído antes da confirmação do roteiro e dos insumos obrigatórios.

## 5. Referências

[1]: ../../arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
[2]: ../../requisitos/contexto-escopo-objetivos.md "Contexto, problema, justificativa e objetivos"
[3]: ../../requisitos/stakeholders-e-escopo.md "Stakeholders, responsabilidades e fronteiras de escopo"
[4]: ../../requisitos/requisitos-funcionais.md "Requisitos funcionais"
[5]: ../../requisitos/requisitos-nao-funcionais.md "Requisitos não funcionais"
[6]: ../../requisitos/casos-de-uso.md "Casos de uso"
[7]: ../../requisitos/matriz-rastreabilidade-n1.md "Matriz de rastreabilidade da N1"
[8]: metodologia-desenvolvimento.md "Metodologia de desenvolvimento da N1"
[9]: cronograma-n1.md "Cronograma acadêmico da N1"
