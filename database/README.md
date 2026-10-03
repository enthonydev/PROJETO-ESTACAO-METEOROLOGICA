# Banco de dados

Persistência PostgreSQL da Estação Meteorológica Inteligente.

## Schema

A migration inicial está em:

```text
database/migrations/001_schema_inicial.sql
```

Ela cria:

- `stations`;
- `measurements`;
- `measurement_quality`;
- índice temporal por estação.

O modelo preserva a qualidade individual das métricas e não define calibrações ou faixas físicas que ainda não tenham sido validadas.

## Execução

Com um PostgreSQL disponível e `DATABASE_URL` configurada no backend, aplique a migration antes de iniciar a aplicação.

Exemplo com `psql`:

```bash
psql "$DATABASE_URL" -f database/migrations/001_schema_inicial.sql
```

O backend seleciona automaticamente a implementação PostgreSQL quando `DATABASE_URL` existe. Sem essa variável, utiliza o repositório em memória para desenvolvimento.

## Estado de validação

A implementação PostgreSQL está integrada ao código e coberta pela mesma interface de repositório. A execução contra uma instância PostgreSQL real depende de infraestrutura de banco disponível e deve ser registrada separadamente como evidência de runtime.
