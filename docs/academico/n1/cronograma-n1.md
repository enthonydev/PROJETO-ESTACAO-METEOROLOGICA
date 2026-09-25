# Cronograma acadêmico da N1

## 1. Objetivo

Este documento atende à task J-S2-04 da Sprint 2. Ele transforma o calendário do plano operacional de James em um cronograma de acompanhamento da N1, preservando as datas fornecidas no documento oficial e explicitando dependências e bloqueios.

As datas abaixo são as datas do plano `N1_Sprints_James_v2.docx`. Não foram acrescentadas datas externas ou prazos inventados.

## 2. Calendário global

| Etapa | Período | Objetivo |
|---|---|---|
| Sprint 1 — Especificação e baseline | 24–25/09/2026 | Fechar escopo, requisitos, arquitetura, contratos e projeto físico antes das partes dependentes. |
| Sprint 2 — Projeto técnico e protótipo | 26–27/09/2026 | Transformar a baseline em artefatos técnicos demonstráveis, protótipos e estruturas iniciais. |
| Sprint 3 — Implementação mínima, testes e evidências | 28–29/09/2026 | Produzir o mínimo integrado necessário à N1 e evidências reais ou simuladas claramente identificadas. |
| Sprint 4 — Consolidação acadêmica da N1 | 30/09/2026 | Consolidar metodologia, requisitos, diagramas, modelagem, protótipos, testes, cronograma e fundamentação. |
| Sprint 5 — Auditoria e fechamento | 01/10/2026 | Revisar, corrigir bloqueadores e congelar a versão candidata à entrega. |
| Entrega | 02/10/2026 | Realizar validação final, correções críticas, empacotamento e submissão. Nenhuma feature nova. |

## 3. Entregas da Sprint 1

| Task | Artefato ou resultado | Estado atual |
|---|---|---|
| J-S1-01 | Contexto, problema, justificativa e objetivos | Documentado e integrado à `main`. |
| J-S1-02 | Stakeholders e escopo | Documentado e integrado à `main`; responsabilidades específicas de Enthony e Luan ainda precisam ser confirmadas. |
| J-S1-03 | Requisitos funcionais | Documentado e integrado à `main`. |
| J-S1-04 | Requisitos não funcionais | Documentado e integrado à `main`. |
| J-S1-05 | Casos de uso | Documentado e integrado à `main`. |

## 4. Entregas da Sprint 2 sob responsabilidade de James

| Task | Entrega | Dependência | Estado desta frente |
|---|---|---|---|
| J-S2-01 | Matriz de rastreabilidade requisito → implementação → teste → evidência | Contrato de Enthony e plano/artefatos de Luan | Matriz inicial produzida; relações dependentes permanecem explicitamente bloqueadas ou pendentes. |
| J-S2-02 | Metodologia de desenvolvimento | Governança e sprints definidas | Concluída documentalmente na branch da Sprint 2. |
| J-S2-03 | Fundamentação teórica | Fontes confiáveis disponíveis | Em elaboração; somente fontes verificáveis serão incorporadas. |
| J-S2-04 | Cronograma acadêmico | Plano operacional da N1 | Concluído com as datas oficiais do plano. |
| J-S2-05 | Estrutura do documento N1 | Roteiro do professor e insumos de Enthony/Luan | Estrutura proposta com pendências explícitas; a estrutura final aguarda confirmação dos insumos. |

## 5. Dependências de outras frentes

A Sprint 2 foi integrada à `main`. A main atual contém o skeleton de backend, fixtures de telemetria, serviço de validação, DER inicial, migration inicial, firmware estrutural e testes técnicos de contrato e tasks. Esses artefatos podem ser tratados como integrados, mas MQTT, persistência runtime, dashboard, pinagem, calibração e evidências físicas continuam pendentes ou bloqueados conforme a matriz da Sprint 3.

Não foi localizado plano ou artefato de Luan no repositório ou na pasta do Drive consultada. Portanto, tarefas que dependam de pinout, componentes, calibração, teste físico ou evidência de bancada devem manter o estado BLOQUEADO até o fornecimento do insumo correspondente.

## 6. Caminho crítico da N1

O caminho crítico permanece:

```text
REQUISITOS → CONTRATO DE DADOS → FIRMWARE → INGESTÃO → BANCO → API → DASHBOARD → TESTES DE CAMPO → RESULTADOS/N2
```

A documentação, o contrato e o backend com fixtures podem avançar sem hardware físico quando a atividade não depender de validação de bancada. A conclusão de integração física, entretanto, não pode ser inferida a partir desses artefatos.

## 7. Gate da Sprint 2

O Gate da Sprint 2 foi encerrado com a integração das frentes aplicáveis na `main`. A Sprint 3 atualiza a matriz, consolida arquitetura e dados, documenta protótipo e testes e relaciona as disciplinas. A integração desta frente continua sujeita à fila oficial e à revisão centralizada; não autoriza merge feito por este PO.

## 8. Referências

[1]: https://docs.google.com/document/d/1ij1nmvs1P_PxaeunHD-nefCdfW433h46/edit "Plano operacional N1 — Sprints James v2"
[2]: ../../arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
[3]: ../../requisitos/matriz-rastreabilidade-n1.md "Matriz de rastreabilidade da N1"
