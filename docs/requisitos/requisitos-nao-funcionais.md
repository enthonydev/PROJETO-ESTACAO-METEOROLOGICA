# Requisitos não funcionais

## 1. Objetivo

Este documento atende à task J-S1-04 da Sprint 1. Os requisitos não funcionais definem propriedades de qualidade, restrições e condições de operação que complementam os requisitos funcionais.

## 2. Requisitos de qualidade e restrições

| ID | Requisito | Prioridade | Critério de aceite inicial |
|---|---|---:|---|
| RNF-01 | O sistema deve manter separação entre drivers, serviços, tarefas, modelos, API, schemas, serviços de negócio, repositórios e apresentação. | P0 | A estrutura do código permite localizar cada responsabilidade sem acoplamento direto entre display e sensor/API. |
| RNF-02 | O firmware deve executar ciclos independentes para aquisição, relógio, consulta meteorológica, sincronização temporal, renderização e publicação. | P0 | Uma falha ou atraso de uma função não bloqueia indefinidamente as demais; a estratégia definitiva deve ser validada no ESP32. |
| RNF-03 | O sistema deve operar de forma degradada quando Wi-Fi, API externa, sensor, display ou TCA9548A estiver indisponível. | P0 | O componente afetado apresenta estado de falha e as funções independentes continuam operando quando possível. |
| RNF-04 | O backend deve ser implementado com Python e FastAPI como baseline. | P0 | A aplicação expõe o healthcheck e os endpoints baseline por meio do framework aprovado. |
| RNF-05 | O armazenamento de produção deve usar PostgreSQL; SQLite é permitido apenas para desenvolvimento ou testes quando preservar a semântica do modelo. | P0 | O modelo relacional, as chaves estrangeiras e os índices permanecem compatíveis entre os ambientes. |
| RNF-06 | O timestamp deve seguir uma política única, preferencialmente UTC no armazenamento e conversão na apresentação. | P0 | A política está documentada e é aplicada de modo consistente no firmware, backend, banco e dashboard. |
| RNF-07 | O índice principal de medições deve contemplar `station_id` e `measured_at`. | P0 | O modelo ou migração documenta o índice e sua finalidade para consultas históricas. |
| RNF-08 | O dashboard deve ser separado do banco de dados e consumir somente a API REST. | P0 | Não há credencial ou conexão do frontend diretamente com PostgreSQL. |
| RNF-09 | O dashboard deve ser responsivo e atender requisitos básicos de acessibilidade. | P0 | São verificadas responsividade, contraste, navegação por teclado, labels, semântica e textos alternativos quando aplicável. |
| RNF-10 | Todas as entradas externas devem ser validadas no limite correspondente. | P0 | Payload MQTT, parâmetros da API, configuração e dados de integração têm validação e tratamento de erro documentados. |
| RNF-11 | O sistema não deve versionar credenciais, SSIDs, senhas, tokens ou arquivos `.env` reais. | P0 | O repositório contém apenas arquivos de exemplo e não expõe segredos em código ou logs. |
| RNF-12 | Os logs devem ser objetivos e úteis para diagnóstico, sem expor segredos. | P0 | Firmware e backend registram inicialização, falhas, conexão, publicação, ingestão inválida e dependências críticas. |
| RNF-13 | O schema de telemetria deve ser versionado e mudanças incompatíveis devem ser escaladas antes da implementação. | P0 | A versão do payload é explícita e existe decisão de compatibilidade para alterações incompatíveis. |
| RNF-14 | Testes devem cobrir drivers e validações, serialização, ingestão, persistência, API, frontend, integração ponta a ponta, operação offline e recuperação. | P0 | Cada caso de teste informa requisito, pré-condição, passos, resultado esperado, resultado obtido, status e evidência. |
| RNF-15 | Evidências de simulação e evidências físicas devem ser identificadas separadamente. | P0 | Cada evidência informa o ambiente e não é apresentada como validação física quando foi produzida por simulação. |
| RNF-16 | O desenvolvimento deve ocorrer em branch de task, com revisão por Pull Request e sem push direto na `main`. | P0 | O histórico e o PR demonstram branch apropriada, revisão, checks aplicáveis e ausência de alteração direta na `main`. |
| RNF-17 | Commits devem ter título, descrição e autoria humana configurada pelo PO, todos em português. | P0 | O commit possui título e corpo em português e usa `Noesis-Ethos <jamesx235xp@gmail.com>` quando o trabalho for deste ambiente. |
| RNF-18 | Alterações relevantes de arquitetura, contratos, tecnologias, banco, schema ou fluxo de integração devem ser registradas em ADR. | P0 | Nenhuma alteração relevante é implementada enquanto o ADR estiver apenas como proposta. |
| RNF-19 | A documentação acadêmica deve permanecer rastreável aos requisitos, implementação, testes, evidências e entregas N1/N2. | P0 | A matriz de rastreabilidade identifica cada relação ou registra a pendência correspondente. |
| RNF-20 | O sistema deve ser demonstrável de forma reproduzível, distinguindo limitações conhecidas e resultados obtidos. | P0 | A documentação informa configuração, ambiente, dados usados, procedimento, resultado e limitações sem inventar evidências. |

## 3. Restrições arquiteturais

O MQTT é o caminho principal de telemetria. A API REST serve o dashboard e os serviços de consulta, mas não substitui a coleta MQTT na produção. Um fallback HTTP só pode existir se for documentado e não criar dois fluxos concorrentes de produção.

O backend é a autoridade de integridade dos dados, embora o firmware também deva validar leituras antes da publicação. O dashboard não acessa o banco diretamente. Os displays recebem estados preparados e não executam aquisição ou sincronização por conta própria.

## 4. Pendências de qualidade

A escolha definitiva de `uasyncio` ou outra estratégia cooperativa depende de validação no ESP32 real. As faixas numéricas dependem de datasheets, calibração e testes. O nível de acessibilidade a ser demonstrado deve ser compatível com o roteiro do professor, caso exista exigência adicional.

## 5. Referências

[1]: ../arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
