# Stakeholders, responsabilidades e fronteiras de escopo

## 1. Objetivo

Este documento atende à task J-S1-02 da Sprint 1. Ele identifica as partes interessadas conhecidas, registra suas responsabilidades documentadas e delimita as fronteiras do produto. Atribuições que não foram definidas nos guias permanecem como **TBD** e precisam ser confirmadas pelos POs.

## 2. Stakeholders identificados

| Stakeholder | Interesse no projeto | Participação conhecida | Ponto que requer confirmação |
|---|---|---|---|
| James | Coerência do produto, documentação, integração e entregas acadêmicas | PO de Produto, Documentação e Integração | Critérios e prioridades dentro da baseline |
| Enthony | Software, arquitetura e integração técnica | PO de Software e Arquitetura | Validação das decisões técnicas que cruzam firmware, backend, contrato e integração |
| Luan | Hardware, sensores e validação física | PO de Hardware, Sensores e Validação Física | Validação elétrica, montagem, caracterização e testes físicos previstos para N2 |
| Luiz Manoel | Participação na equipe do projeto | Integrante da equipe | Atribuições específicas não formalizadas nos guias operacionais |
| Professor da disciplina | Avaliação acadêmica e definição dos critérios de N1/N2 | Define o roteiro, os requisitos acadêmicos e os critérios de entrega | Calendário e rubrica final de N1/N2, se houver material adicional |
| Usuário público do dashboard | Consulta das condições ambientais e do histórico disponível | Consome a API por meio do dashboard web | Perfis de uso e necessidades específicas ainda não detalhados |
| Responsáveis por hardware/firmware | Validação física, aquisição, conectividade e operação embarcada | Enthony responde pela integração técnica e Luan pela frente física, com revisão cruzada quando a decisão atravessa as duas áreas | Modelos reais, níveis elétricos, pinagem definitiva e evidências físicas dependem da etapa de bancada |

## 3. Responsabilidades de governança

James conduz escopo, backlog, priorização, critérios de aceite, requisitos, roadmap, rastreabilidade, integração entre frentes e preparação de N1/N2. Ele também consolida evidências, resultados, limitações e documentação final.

Decisões elétricas críticas, alterações centrais de firmware e mudanças arquiteturais que atravessem fronteiras entre frentes não devem ser aprovadas isoladamente por James. Nessas situações, os responsáveis afetados devem participar da decisão e, quando aplicável, deve ser criado um ADR.

A revisão de cada task deve ser solicitada explicitamente a um dos POs: James, Enthony ou Luan. O merge na `main` somente pode ocorrer após as revisões e checks previstos na governança do projeto.

## 4. Fronteira do produto

O produto inclui o caminho completo entre aquisição e visualização:

```text
Sensores → ESP32 → Wi-Fi/MQTT → Backend → PostgreSQL → API REST → Dashboard
```

Também inclui uma OLED I²C local, a sincronização NTP e a integração complementar com uma API meteorológica externa. A baseline não inclui segunda OLED, DS3231 ou TCA9548A, conforme o ADR-002.

O produto não inclui, no MVP, previsão por aprendizado de máquina, rede mesh, aplicativo mobile nativo, sistema de energia solar como requisito obrigatório, caixa IP65 definitiva ou alertas multicanal de produção.

## 5. Fronteiras entre componentes

### 5.1 Hardware e firmware

O hardware fornece sinais dos sensores, da interface local e das interfaces elétricas. O firmware realiza aquisição, validação, conectividade, serialização, publicação e renderização local. A pinagem final, as características do módulo de chuva, a caracterização do MQ-135 e os limites elétricos dependem de validação física.

### 5.2 Firmware e backend

A fronteira é o tópico MQTT e o payload JSON versionado. O firmware deve publicar no tópico `estacao/<station_id>/telemetry`. O backend é a autoridade de integridade e deve validar novamente o schema, o timestamp, a estação e os valores recebidos.

### 5.3 Backend, banco e API

O backend recebe e valida telemetria, aplica regras de negócio, persiste dados e fornece consultas. O frontend não acessa o PostgreSQL diretamente. A API REST é a única fronteira prevista entre o dashboard e o backend.

### 5.4 Dashboard e usuário público

O dashboard apresenta dados atuais, históricos, localização e estados de carregamento, erro ou ausência de dados. Um valor zero não deve ser usado silenciosamente para representar dado ausente.

### 5.5 Documentação e evidências

A documentação deve relacionar requisitos, arquitetura, implementação, testes e evidências. Evidências de simulação e de bancada física devem ser identificadas separadamente.

## 6. Dependências cruzadas conhecidas

As decisões abaixo dependem de outros responsáveis ou de validação adicional:

- requisitos que cruzem software e hardware dependem de revisão conjunta de Enthony e Luan;
- pinagem depende de validação elétrica e dos componentes reais;
- qualquer método de conversão quantitativa da chuva depende do módulo real e de validação experimental;
- interpretação do MQ-135 depende de calibração defensável;
- contrato de telemetria depende de alinhamento entre firmware e backend;
- cronograma final depende do calendário e da rubrica do professor;
- evidências técnicas dependem dos artefatos produzidos pelas demais frentes.

Quando uma dependência bloquear uma task, o bloqueio deve registrar o ID da task, o responsável e o artefato necessário. Não se deve alterar a área de outro PO para contornar o bloqueio.

## 7. Referências

[1]: ../arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
