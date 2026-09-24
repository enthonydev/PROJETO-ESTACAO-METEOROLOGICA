# Contribuindo

## Branches

Nunca desenvolva diretamente na `main`. Use uma branch com prefixo compatível com o trabalho:

- `feature/` para funcionalidade;
- `fix/` para correção;
- `docs/` para documentação;
- `chore/` para manutenção ou infraestrutura;
- `test/` para testes;
- `refactor/` para refatoração sem mudança funcional.

O nome deve descrever o escopo de forma curta e não deve conter referências a pessoas, ferramentas ou processos automatizados.

## Commits

Cada commit deve representar uma unidade coerente de mudança. O título e a descrição devem ser escritos em português e informar o impacto relevante. Evite mensagens genéricas como `update`, `ajustes` ou `teste`.

Antes do primeiro commit de um ambiente, a identidade Git do integrante responsável deve ser confirmada. Credenciais, tokens, senhas, SSIDs e arquivos `.env` nunca devem ser versionados.

## Pull Requests

Toda alteração deve ser revisada antes de ser integrada à `main`. A descrição do Pull Request deve informar escopo, testes executados, limitações, dependências cruzadas e eventual impacto arquitetural.

Não faça merge sem revisão do PO responsável, checks aplicáveis aprovados e autorização explícita.

## Arquitetura e contratos

Alterações em tecnologias baseline, fluxo de integração, tópicos MQTT, schema de telemetria, API, modelo de dados ou responsabilidades entre camadas exigem registro em `docs/arquitetura/adr/` e revisão antes da implementação.

O dashboard não acessa o banco diretamente. O backend valida novamente toda telemetria recebida. Valores ausentes ou inválidos não devem ser substituídos silenciosamente por zero ou por outro valor inventado.

## Testes e evidências

Execute os testes aplicáveis à alteração. Diferencie evidências simuladas de evidências físicas e registre limitações conhecidas na documentação da task.
