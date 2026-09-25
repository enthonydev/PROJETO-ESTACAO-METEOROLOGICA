# Matriz de rastreabilidade da N1

## 1. Objetivo e estado

Este documento atende à task J-S2-01 da Sprint 2. A matriz relaciona requisitos aos artefatos, testes e evidências previstos para a N1. Ela deve ser atualizada quando as frentes de backend, hardware e firmware fornecerem artefatos revisados.

**Estado desta versão:** matriz inicial ativa. A documentação e o contrato estão disponíveis. Os artefatos técnicos de backend e banco de dados de Enthony foram identificados na branch `feature/sprint-2-backend-modelo-dados`, mas ainda não estão integrados à `main`. Não foi localizado plano ou artefato de Luan no repositório ou no Drive consultado. As partes que dependem de hardware, pinout, calibração ou teste físico permanecem bloqueadas.

## 2. Legenda

| Estado | Significado |
|---|---|
| Documentado | Existe requisito ou artefato documental versionado. |
| Implementado — branch técnica | Existe implementação identificada em branch ainda não integrada. |
| Validado em software | Existe teste executável ou inspeção reproduzível correspondente. |
| Simulado | Evidência produzida em ambiente simulado ou com dados sintéticos. |
| Bloqueado | A conclusão depende de insumo ou validação ainda inexistente. |
| Pendente | A relação ainda precisa ser preenchida quando a frente fornecer o artefato. |

## 3. Requisitos funcionais

| ID | Requisito resumido | Artefato relacionado | Teste/evidência | Estado e dependência |
|---|---|---|---|---|
| RF-01 | Identificar estação por `station_id`. | Contrato v1.0; schema backend | Fixture válida e estação desconhecida | Implementado — branch técnica; integração pendente |
| RF-02 | Adquirir temperatura e umidade. | Arquitetura; firmware a fornecer | Teste de sensor e fixture | Bloqueado para validação física; software pendente |
| RF-03 | Adquirir pressão atmosférica. | Arquitetura; firmware a fornecer | Teste de sensor e fixture | Bloqueado para validação física; software pendente |
| RF-04 | Adquirir indicador de qualidade do ar. | Contrato; documentação de sensor | Teste de valor bruto e qualidade | Bloqueado por calibração/interpretação; não converter por suposição |
| RF-05 | Adquirir luminosidade. | Contrato; documentação de sensor | Teste de leitura e unidade | Bloqueado por validação de hardware e unidade final |
| RF-06 | Adquirir precipitação. | Contrato; documentação do pluviômetro | Teste de pulsos e conversão | Bloqueado por modelo e fator de conversão do pluviômetro |
| RF-07 | Registrar timestamp e estação. | Contrato v1.0; schema backend | Payload válido e timestamp inválido | Implementado — branch técnica; integração pendente |
| RF-08 | Validar leituras e qualidade no firmware. | Requisitos; firmware a fornecer | Casos de falha e qualidade | Pendente de firmware; faixas físicas ainda não definidas |
| RF-09 | Publicar telemetria por Wi-Fi/MQTT. | Contrato de integração | Fixture e teste de publicação | Pendente de firmware/broker; contrato documentado |
| RF-10 | Reconectar sem bloquear funções. | Arquitetura; metodologia | Teste offline/recuperação | Bloqueado para validação no hardware; desenho documentado |
| RF-11 | Validar telemetria no backend. | `backend/app/schemas`; serviço de validação | `backend/tests/test_api.py` | Implementado — branch técnica; integração pendente |
| RF-12 | Persistir medição e qualidade. | DER e migration iniciais | Teste de persistência e integridade | Implementado — branch técnica; execução/integracão pendente |
| RF-13 | Expor saúde, estações, última leitura, histórico e resumo. | Requisitos; arquitetura | Testes de API | Healthcheck/validação parcial na branch técnica; endpoints restantes pendentes |
| RF-14 | Exibir métricas atuais. | Requisitos; frontend a fornecer | Fixture e teste de interface | Pendente de frontend |
| RF-15 | Consultar histórico por período. | API baseline; frontend a fornecer | Teste de filtro e interface | Pendente de backend/API/frontend |
| RF-16 | Representar localização aprovada. | Schema; DER | Teste com coordenadas aprovadas | Bloqueado pelas coordenadas físicas ainda não definidas |
| RF-17 | Exibir loading, erro e ausência de dados. | Requisitos; frontend a fornecer | Testes de estados da interface | Pendente de frontend |
| RF-18 | Exibir estado meteorológico local e externo. | Arquitetura de telas | Teste online/offline | Bloqueado por firmware, API e validação física |
| RF-19 | Exibir relógio e calendário. | Arquitetura de telas | Teste de display e serviço de tempo | Bloqueado por firmware e hardware |
| RF-20 | Sincronizar NTP e manter DS3231 offline. | Arquitetura de telas | Teste online/offline | Bloqueado por hardware e firmware |
| RF-21 | Controlar displays por canais do TCA9548A. | Arquitetura de telas | Teste de canais I2C | Bloqueado por pinout e hardware |
| RF-22 | Isolar falhas parciais. | Metodologia; arquitetura | Testes de falha e recuperação | Pendente de firmware e integração |
| RF-23 | Registrar falhas relevantes. | Requisitos; metodologia | Inspeção de logs | Backend parcial na branch técnica; firmware/frontend pendentes |

## 4. Requisitos não funcionais

| ID | Requisito resumido | Artefato relacionado | Teste/evidência | Estado e dependência |
|---|---|---|---|---|
| RNF-01 | Separar responsabilidades por camadas. | Arquitetura; estrutura oficial | Inspeção estrutural | Documentado; backend parcial em branch técnica |
| RNF-02 | Manter ciclos independentes. | Arquitetura; metodologia | Teste de concorrência/recuperação | Bloqueado para validação no ESP32 |
| RNF-03 | Operar de forma degradada. | Arquitetura; metodologia | Testes offline/recuperação | Bloqueado por hardware/firmware; desenho documentado |
| RNF-04 | Usar Python/FastAPI no backend. | ADR-001; backend técnico | Testes da aplicação | Implementado — branch técnica; integração pendente |
| RNF-05 | Usar PostgreSQL com compatibilidade de modelo. | ADR-001; migration | Teste de schema/migration | Implementado — branch técnica; execução pendente |
| RNF-06 | Usar política temporal única. | Arquitetura; DER | Inspeção e teste temporal | Documentado; migration usa `TIMESTAMPTZ` na branch técnica |
| RNF-07 | Indexar estação e instante. | DER; migration | Inspeção de índice | Implementado — branch técnica; integração pendente |
| RNF-08 | Separar dashboard do banco. | Arquitetura; metodologia | Inspeção de configuração | Pendente de frontend |
| RNF-09 | Dashboard responsivo e acessível. | Requisitos; frontend a fornecer | Teste de interface | Pendente de frontend |
| RNF-10 | Validar entradas externas. | Contrato; schema e serviço backend | Fixtures válidas, parciais e inválidas | Validado em software na branch técnica; integração pendente |
| RNF-11 | Não versionar segredos. | `.gitignore`; SECURITY | Inspeção do repositório | Documentado; verificação contínua |
| RNF-12 | Produzir logs úteis sem segredos. | Requisitos; backend técnico | Inspeção de logs | Parcial; firmware e frontend pendentes |
| RNF-13 | Versionar schema e compatibilidade. | Contrato v1.0 | Validação JSON e contrato | Validado em software no baseline; integração pendente |
| RNF-14 | Cobrir camadas de teste. | Metodologia; testes a fornecer | Casos de teste e CI | Parcial; somente baseline/backend disponíveis |
| RNF-15 | Separar evidência física e simulada. | Metodologia; evidências | Inspeção dos registros | Documentado; evidências ainda pendentes |
| RNF-16 | Trabalhar por branch e PR. | CONTRIBUTING; metodologia | Histórico e PR | Documentado e aplicado nesta branch |
| RNF-17 | Commits em português e autoria autorizada. | Governança; histórico Git | Inspeção do commit | Aplicado nesta branch |
| RNF-18 | Registrar mudanças relevantes em ADR. | ADR-001; metodologia | Inspeção da decisão | Documentado; ADR permanece proposto para revisão |
| RNF-19 | Manter rastreabilidade até N1/N2. | Esta matriz; estrutura N1 | Revisão cruzada | Em execução; dependente de artefatos das frentes |
| RNF-20 | Garantir demonstração reproduzível. | Metodologia; evidências | Checklist e procedimento | Pendente de protótipo e evidências reais/simuladas |

## 5. Dependências cruzadas

A matriz pode ser atualizada com os artefatos de Enthony identificados na branch técnica, mas não deve apresentar esses artefatos como integrados antes da revisão e do merge centralizado. O plano ou artefato de Luan não foi localizado; por isso, as relações que exigem pinout, hardware ou evidência física permanecem bloqueadas.

A ausência de hardware não bloqueia a documentação dos requisitos, contratos, metodologia e testes de software. Ela bloqueia apenas as conclusões que dependem de leitura física, pinagem, calibração, operação offline no dispositivo real ou evidência de bancada.

## 6. Critério de atualização

Cada nova linha deve informar o artefato exato, o tipo de teste, o ambiente da evidência e o responsável pela revisão. Uma relação não deve ser marcada como validada apenas porque o código foi criado. A classificação deve acompanhar a evidência disponível.

## 7. Referências

[1]: ../arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
[2]: ../contratos/contratos-integracao.md "Contratos de integração"
[3]: ../contratos/telemetria-v1.0.json "Contrato de telemetria v1.0"
[4]: ../arquitetura/adr/ADR-001-baseline-tecnica.md "ADR-001 — Baseline técnica do sistema"
[5]: requisitos-funcionais.md "Requisitos funcionais"
[6]: requisitos-nao-funcionais.md "Requisitos não funcionais"
[7]: ../academico/n1/metodologia-desenvolvimento.md "Metodologia de desenvolvimento da N1"
