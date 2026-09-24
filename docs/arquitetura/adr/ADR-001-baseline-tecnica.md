# ADR-001 — Baseline técnica do sistema

- **Status:** Proposto para revisão dos POs
- **Data:** 2026-09-24
- **Escopo:** firmware, telemetria, backend, persistência e dashboard

## Contexto

O projeto precisa de uma baseline comum para que firmware, integração, backend, banco de dados e dashboard evoluam sem contratos incompatíveis. A solução deve atender ao fluxo acadêmico de coleta ambiental, transmissão, persistência, consulta e visualização pública.

As decisões desta ADR derivam do Guia Mestre do Projeto, da arquitetura versionada em `docs/arquitetura/arquitetura-sistema.md` e do contrato de telemetria v1.0.

## Opções consideradas

### Opção 1 — HTTP direto do ESP32 ao backend

Simplifica um protótipo local, mas acopla a estação física ao servidor e não atende ao caminho principal de telemetria definido para o projeto.

### Opção 2 — MQTT para telemetria e REST para consulta

Desacopla a estação do backend, é adequada à telemetria IoT e permite que o dashboard consuma uma API estável sem acessar o banco diretamente.

### Opção 3 — Armazenamento em arquivo ou banco não relacional

Reduz a configuração inicial, mas não atende ao baseline de persistência relacional, integridade, histórico e modelagem exigido para a N1.

## Decisão proposta

Adotar a seguinte baseline:

| Área | Decisão |
| --- | --- |
| Microcontrolador | ESP32 DevKit V1 |
| Firmware | MicroPython |
| Conectividade | Wi-Fi |
| Telemetria | MQTT |
| Tópico | `estacao/<station_id>/telemetry` |
| Contrato | JSON versionado, atualmente `1.0` |
| Backend | Python com FastAPI |
| Persistência | PostgreSQL |
| API para o dashboard | REST em `/api/v1` |
| Dashboard | Web responsivo e desacoplado do banco |

O fluxo oficial é:

```text
Sensores → ESP32/MicroPython → Wi-Fi → MQTT → Backend/FastAPI → PostgreSQL → API REST → Dashboard
```

O backend será a autoridade de validação na fronteira de ingestão. Mensagens incompatíveis, timestamps inválidos e estações desconhecidas não serão corrigidos ou associados silenciosamente.

## Consequências

A separação MQTT/REST permite desenvolver e testar o backend com fixtures antes da disponibilidade do hardware completo. Em contrapartida, será necessário manter o contrato versionado e testar a ingestão separadamente da API.

PostgreSQL exige modelagem, migrations e testes de integridade. SQLite poderá apoiar testes locais somente quando preservar a semântica do modelo.

O dashboard dependerá dos endpoints do backend e não poderá consultar PostgreSQL diretamente.

A escolha não congela decisões ainda pendentes sobre pinagem, modelo e conversão do pluviômetro, calibração do MQ-135, infraestrutura do broker, coordenadas da estação, faixas numéricas ou periodicidades exatas.

## Impacto

A decisão orienta os diretórios `firmware/`, `backend/`, `frontend/`, `database/` e `docs/`. Ela também estabelece a fronteira de integração entre Luan, Enthony e James, sem substituir requisitos, evidências físicas ou decisões de hardware.

Mudanças de tecnologia, troca do transporte principal, alteração incompatível do contrato, mudança do modelo de dados ou criação de uma nova camada estrutural exigem nova ADR ou atualização formal desta decisão antes da implementação.

## Validação e aprovação

Esta ADR deve ser revisada pelos POs responsáveis. Enquanto permanecer com status **Proposto**, nenhuma mudança arquitetural derivada dela deve ser tratada como aprovada.

Após a revisão, registrar a decisão dos POs, eventuais ressalvas e a atualização do status neste arquivo.

## Referências internas

- `docs/arquitetura/arquitetura-sistema.md`
- `docs/contratos/contratos-integracao.md`
- `docs/contratos/telemetria-v1.0.json`
