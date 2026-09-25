# Metodologia de desenvolvimento da N1

## 1. Objetivo

Este documento atende à task J-S2-02 da Sprint 2. Ele define como o projeto será planejado, desenvolvido, validado, revisado e integrado durante a preparação da entrega N1.

A metodologia combina execução incremental por sprints, rastreabilidade entre requisitos e evidências, revisão por Pull Request e escalonamento de dependências reais. Ela não substitui decisões técnicas da arquitetura nem autoriza a conclusão de tarefas que dependam de validação física, calibração ou artefatos ainda não fornecidos.

## 2. Princípios de execução

O trabalho deve permanecer orientado ao MVP e aos critérios de N1. Cada task precisa ter objetivo, responsável, dependências, critérios de aceite e artefatos esperados antes do início.

Tasks independentes podem avançar em paralelo. Uma dependência deve bloquear somente a task ou a parte que realmente precisa dela. A indisponibilidade de hardware não bloqueia documentação ou software que possam ser produzidos sem validação física.

Nenhum resultado pode ser inventado para remover um bloqueio. A documentação deve diferenciar o que foi projetado, implementado, simulado, validado em software e validado fisicamente.

## 3. Ciclo de trabalho por sprint

Cada sprint segue um ciclo de preparação, execução, validação e Gate.

### 3.1 Preparação

Antes de iniciar uma task, o responsável deve atualizar sua visão da `main`, confirmar a sprint atual, inspecionar a estrutura oficial do repositório e verificar dependências específicas. A branch de trabalho deve ser criada a partir da `main` atualizada e não deve reutilizar a branch de outra sprint.

A task só está pronta para começar quando o objetivo, responsável, critérios de aceite, dependências e contrato relevante estiverem identificados. Se uma decisão arquitetural estiver pendente e for necessária para começar, a task deve permanecer bloqueada.

### 3.2 Execução

A implementação deve alterar somente os arquivos necessários para os critérios de aceite. Os artefatos devem ser colocados nos diretórios oficiais já existentes. Não devem ser criados diretórios equivalentes, nem reorganizada a estrutura global sem autorização.

Quando a alteração afetar arquitetura, contrato de integração, schema, tecnologia baseline, modelo de dados ou fluxo entre componentes, a task deve ser escalada e um ADR deve ser produzido antes da implementação correspondente.

### 3.3 Validação

A validação deve usar o nível de evidência adequado ao artefato. Documentos são verificados quanto a coerência, rastreabilidade e aderência aos guias. Código é verificado por testes aplicáveis. Simulações são identificadas como simulações. Resultados de bancada e testes físicos somente podem ser declarados quando existirem evidências físicas correspondentes.

Cada caso de teste deve registrar ID, requisito relacionado, pré-condição, passos, dados, resultado esperado, resultado obtido, status e evidência. As limitações e pendências devem permanecer visíveis quando impedirem uma conclusão completa.

### 3.4 Gate

Ao concluir a parte aplicável de uma sprint, deve ser produzido um relatório de Gate com tasks, status, branch, arquivos, testes, evidências, dependências liberadas, bloqueios e revisão solicitada. O Gate somente pode ser declarado integralmente concluído quando todos os requisitos obrigatórios estiverem atendidos. Se houver uma pendência externa, o Gate deve informar quais frentes foram concluídas e qual parte permanece bloqueada.

Não se deve avançar automaticamente para a sprint seguinte. A autorização do PO é necessária para liberar a próxima etapa conforme o plano operacional da N1.

## 4. Governança Git e Pull Request

O desenvolvimento ocorre fora da `main`, em branch específica da task ou da frente. Antes de qualquer push, deve ser verificado se a branch está baseada no estado correto da `main`, se os arquivos estão nos diretórios oficiais, se não há segredos e se as dependências da task foram respeitadas.

Cada commit deve representar uma unidade coerente de mudança, possuir título e descrição em português e usar a identidade humana autorizada para o ambiente. O Pull Request deve usar o template oficial, registrar o escopo, as dependências, os testes, a classificação das evidências, o impacto arquitetural e o estado do Gate.

A integração na `main` é centralizada. A abertura ou atualização de um Pull Request não autoriza merge automático. Em caso de dúvida, conflito ou dependência não confirmada, a integração deve aguardar validação do PO.

## 5. Responsabilidades e revisão

James conduz produto, documentação acadêmica, integração, critérios de aceite e rastreabilidade. Enthony e Luan fornecem ou revisam os artefatos de suas frentes conforme as responsabilidades que forem confirmadas para cada task.

Uma task que dependa de hardware, pinout, calibração, teste físico ou evidência de outra frente deve registrar o responsável e o artefato necessário. Nenhum PO deve modificar a área de outro PO para contornar a dependência.

Ao final de cada task, a revisão deve ser solicitada explicitamente ao PO responsável. A revisão deve verificar escopo, critérios de aceite, consistência arquitetural, evidências, limitações e impacto na N1.

## 6. Definition of Ready

Uma task está pronta para execução quando:

- o objetivo e o responsável estão definidos;
- os critérios de aceite são verificáveis;
- as dependências estão identificadas;
- os contratos ou decisões arquiteturais relevantes foram localizados;
- a branch e os diretórios oficiais estão definidos;
- não existe decisão arquitetural pendente necessária para iniciar;
- o insumo de outro PO foi recebido quando a task realmente depende dele.

## 7. Definition of Done

Uma task pode ser apresentada para revisão quando:

- o artefato atende ao escopo aprovado;
- os testes aplicáveis foram executados;
- as evidências foram registradas e classificadas;
- a documentação e a rastreabilidade foram atualizadas;
- não há segredos ou dados indevidos versionados;
- o commit usa a identidade autorizada e texto em português;
- as pendências e limitações estão explícitas;
- o Pull Request está aberto ou atualizado conforme a governança;
- a revisão do PO foi solicitada.

O merge e a integração na `main` não fazem parte da conclusão autônoma da task. Eles dependem da revisão centralizada e dos checks aplicáveis.

## 8. Classificação de resultados

| Classificação | Significado |
|---|---|
| Projetado | Definido em arquitetura, requisito, contrato, diagrama ou plano, mas ainda não executado. |
| Implementado | Presente em código ou documentação versionada, sem indicar que foi validado em execução. |
| Simulado | Exercitado em ambiente simulado ou com dados sintéticos. |
| Validado em software | Verificado por teste automatizado, teste local ou inspeção técnica reproduzível. |
| Validado fisicamente | Verificado em hardware ou bancada física, com evidência correspondente. |

Uma mesma funcionalidade pode possuir mais de uma classificação em etapas diferentes. A classificação mais forte não deve ser usada sem a evidência necessária.

## 9. Aplicação à Sprint 2

A task J-S2-02 está sendo executada como atividade documental independente. A matriz de rastreabilidade depende de alinhamento com o contrato de integração e com os planos das demais frentes. A fundamentação teórica depende de fontes confiáveis disponíveis e verificáveis. O cronograma e a estrutura final do documento N1 dependem dos insumos e do roteiro acadêmico aplicáveis.

Essas dependências não bloqueiam a metodologia, mas devem ser registradas antes de concluir as tasks correspondentes.

## 10. Referências

[1]: ../../arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
[2]: ../../requisitos/contexto-escopo-objetivos.md "Contexto, problema, justificativa e objetivos"
[3]: ../../requisitos/requisitos-funcionais.md "Requisitos funcionais"
[4]: ../../requisitos/requisitos-nao-funcionais.md "Requisitos não funcionais"
[5]: ../../requisitos/casos-de-uso.md "Casos de uso"
