# Contribuindo

## Branches

Nunca desenvolva diretamente na `main`. Use uma branch com prefixo compatível com o trabalho: `feature/`, `fix/`, `docs/`, `chore/`, `test/` ou `refactor/`.

O nome deve descrever o escopo de forma curta e não deve conter referências a pessoas, ferramentas ou processos automatizados.

## Commits e push

Cada commit deve representar uma unidade coerente. Título e descrição devem ser escritos em português. Antes do primeiro commit de um ambiente, confirme a identidade Git do integrante responsável.

Os responsáveis pelas frentes podem criar branch, commitar e fazer push apenas em suas branches de trabalho. Não devem integrar alterações diretamente na `main`.

Credenciais, tokens, senhas, SSIDs, chaves de API, strings de conexão e arquivos `.env` nunca devem ser versionados.

## Pull Requests e integração

Toda alteração destinada à `main` passa por revisão técnica e pelos checks aplicáveis. A descrição deve informar escopo, testes/evidências, limitações, dependências cruzadas e impacto arquitetural.

A integração na `main` é centralizada pela gestão do repositório após a revisão. Nenhum executor de uma frente deve fazer merge da própria entrega.

Quando existir dependência entre frentes, a ordem padrão de integração é:

1. Hardware, sensores e validação;
2. Software e arquitetura;
3. Produto, documentação e integração acadêmica.

Essa ordem não impede trabalho paralelo dentro da mesma sprint. Ela controla apenas integrações que dependem de artefatos anteriores. Se uma dependência não estiver integrada ou validada, a task dependente permanece bloqueada; não se altera a área de outra frente para contornar o bloqueio.

A conclusão de tasks não libera automaticamente a sprint seguinte. O Gate da sprint deve ser revisado antes do avanço.

## Estrutura do repositório

A árvore-base é mantida centralmente. Antes de criar arquivos, sincronize sua branch com a `main` e use os diretórios existentes. Não renomeie, mova, replique ou exclua diretórios estruturais sem aprovação.

Se uma task exigir novo diretório estrutural, registre a necessidade para revisão antes de criá-lo. Arquivos `.gitkeep` podem ser removidos quando o diretório passar a conter arquivos reais.

## Arquitetura e contratos

Alterações em tecnologias baseline, fluxo de integração, tópicos MQTT, schema de telemetria, API, modelo de dados ou responsabilidades entre camadas exigem ADR e revisão antes da implementação.

O dashboard não acessa o banco diretamente. O backend valida toda telemetria recebida. Valores ausentes ou inválidos não devem ser substituídos silenciosamente por zero ou outro valor inventado.

## Testes e evidências

Execute os testes aplicáveis à alteração. Diferencie evidências físicas, simuladas e de software. Não fabrique resultados, medições, pinagem, calibração ou referências para satisfazer um Gate.
