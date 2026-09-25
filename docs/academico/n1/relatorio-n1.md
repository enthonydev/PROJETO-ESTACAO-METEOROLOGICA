# Estação Meteorológica Inteligente com ESP32
## Relatório acadêmico consolidado da N1

**Curso:** Ciência da Computação — Projeto e Desenvolvimento II (68F3)
**Produto:** Estação Meteorológica Inteligente com ESP32
**Versão documental:** Sprint 4 — consolidação acadêmica da N1
**Estado:** primeira versão consolidada, com resultados de software e projeto técnico; sem validação física dos componentes.

> **Nota de escopo:** este relatório registra somente fatos sustentados por requisitos, documentos, código, testes automatizados, fixtures, auditorias e referências verificáveis presentes no repositório. A documentação, a implementação de software e a simulação não são apresentadas como validação física.

## Resumo

Este relatório apresenta a primeira versão consolidada da N1 de uma Estação Meteorológica Inteligente baseada em ESP32. O projeto propõe um fluxo completo de aquisição, telemetria, persistência e visualização: sensores, firmware em MicroPython, Wi-Fi, MQTT, backend Python, PostgreSQL, API REST e dashboard web. A arquitetura também prevê duas telas OLED locais, sincronização temporal por NTP e referência local por DS3231.

A entrega disponível demonstra uma base documental e de software. O repositório contém requisitos funcionais e não funcionais, casos de uso, contrato de telemetria v1.0, arquitetura, DER, migration SQL, skeleton de firmware, backend FastAPI, fixtures e testes automatizados. Na validação executada, dez testes de backend e sete testes estruturais de firmware passaram. O contrato JSON também foi validado.

Os resultados não demonstram ainda ingestão MQTT, persistência em PostgreSQL executável, dashboard funcional, montagem de sensores, pinagem, calibração, leitura física, operação offline no ESP32 ou teste de campo. Assim, a N1 comprova a coerência da especificação, do modelo e do protótipo de software, mas mantém como pendentes ou bloqueadas as conclusões que dependem de infraestrutura e hardware.

## 1. Contexto, problema e justificativa

O projeto está inserido na disciplina Ciência da Computação — Projeto e Desenvolvimento II (68F3). Seu objetivo acadêmico é integrar sistemas embarcados, comunicação, backend, banco de dados, dashboard web e documentação rastreável [1].

A solução proposta coleta dados ambientais, transmite telemetria, armazena histórico e disponibiliza informações para consulta pública. O fluxo arquitetural é:

```text
Sensores → ESP32/MicroPython → Wi-Fi → MQTT → Backend Python → PostgreSQL → API REST → Dashboard Web
```

O dispositivo também prevê duas interfaces locais. Uma apresenta informações meteorológicas externas e medições locais do BME280. A outra apresenta data, hora e calendário, com correção periódica por NTP e referência local por DS3231 quando a internet estiver indisponível. Essas interfaces complementam o dashboard web.

O problema de engenharia consiste em demonstrar, de forma integrada e rastreável, como uma leitura ambiental pode sair dos sensores, ser validada, ser transmitida, chegar ao backend, ser persistida e ser apresentada ao usuário. Sem contrato comum e critérios de evidência, hardware, firmware, backend, banco, frontend e documentação podem evoluir de forma incompatível.

A justificativa do projeto está na integração de aquisição de dados, IoT, persistência, visualização, validação e engenharia de software em um produto acadêmico único. A rastreabilidade reduz o risco de apresentar como concluído um comportamento que ainda depende de calibração, infraestrutura ou operação física.

## 2. Objetivos

### 2.1 Objetivo geral

Projetar e validar uma estação meteorológica urbana baseada em ESP32 que colete dados ambientais, transmita telemetria, persista histórico e disponibilize informações por API REST e dashboard web público, com documentação e evidências coerentes com os requisitos acadêmicos.

### 2.2 Objetivos específicos

Os objetivos específicos são definir requisitos, stakeholders, casos de uso e critérios de aceite; integrar sensores ao ESP32; implementar aquisição, validação, tratamento de falhas e transmissão; preservar um contrato de telemetria versionado; implementar ingestão, validação, persistência e consulta no backend; modelar o histórico em banco relacional; disponibilizar API e dashboard; implementar as telas OLED; e registrar testes, evidências, limitações e resultados de forma reproduzível [1].

A N1 não declara que todos esses objetivos foram concluídos. Ela registra o estado verificável de cada objetivo na matriz de rastreabilidade e na seção de resultados deste relatório [8].

## 3. Stakeholders e fronteiras de escopo

James conduz produto, documentação acadêmica, integração, critérios de aceite e rastreabilidade. Enthony e Luan participam das frentes técnicas conforme as responsabilidades e os artefatos definidos para cada task. O professor define o roteiro e os critérios acadêmicos. O usuário público consulta as condições ambientais e o histórico disponível pelo dashboard. Os responsáveis por hardware e firmware devem validar decisões elétricas, pinagem, sensores e operação embarcada [2].

O MVP deve coletar temperatura, umidade, pressão, indicador de qualidade do ar, luminosidade e precipitação. Cada amostra deve conter estação e timestamp. O sistema deve validar leituras, registrar qualidade, persistir histórico, expor estado atual e histórico e disponibilizar dashboard público quando as camadas correspondentes existirem.

Não fazem parte do MVP obrigatório previsão por aprendizado de máquina, rede mesh, aplicativo mobile nativo, painel solar e bateria como requisito obrigatório, caixa IP65 definitiva e alertas multicanal de produção. Esses itens podem ser trabalhos futuros.

Permanecem pendentes a pinagem definitiva, o modelo e fator de conversão do pluviômetro, a calibração do MQ-135, a infraestrutura final de broker e hospedagem, as coordenadas físicas, as faixas finais de validação e a decisão sobre sensores com funções sobrepostas [1] [2].

## 4. Fundamentação teórica

### 4.1 Cidades inteligentes e monitoramento ambiental

Revisões sobre sensores em sistemas IoT para cidades inteligentes relacionam monitoramento ambiental, comunicação e análise de dados a aplicações urbanas. Elas também registram desafios de interoperabilidade, ruído, amostras limitadas, privacidade e infraestrutura [7]. A ISO 37122:2019 fornece indicadores e metodologias para mensuração de cidades inteligentes, mas não especifica o hardware nem certifica esta estação [11].

A estação é, portanto, justificável como uma infraestrutura acadêmica de aquisição e disponibilização de dados ambientais. A justificativa não implica que os dados possuam exatidão ou representatividade sem calibração, metadados, controle de qualidade e avaliação do sítio.

### 4.2 ESP32, MicroPython e IoT

A ficha técnica do ESP32 documenta Wi-Fi, Bluetooth, GPIO, ADC, DAC, I2C, SPI, UART, temporizadores, watchdog e modos de baixo consumo [12]. A documentação do MicroPython apresenta APIs para essas interfaces e registra restrições importantes, como o conflito potencial entre ADC2 e Wi-Fi e o uso apenas como entrada de GPIOs 34–39 [7]. Essas fontes sustentam a viabilidade de projeto, mas não validam pinagem, consumo, estabilidade ou desempenho da montagem real.

A especificação MQTT 5.0 sustenta o caminho de telemetria por publicação e assinatura. Ela define QoS 0, QoS 1 e QoS 2 com compromissos diferentes entre perda, duplicação e overhead [13]. O protocolo está documentado no projeto, mas não há consumidor MQTT implementado ou evidência de publicação real na N1.

### 4.3 Qualidade de medições

A literatura de sensores de baixo custo registra riscos de deriva, interferência, montagem, exposição e diferença entre laboratório e campo. Ela recomenda calibração nas condições de implantação, avaliação contínua e comparação com instrumentos de referência quando aplicável [19]. A EPA também recomenda explicitar objetivos de qualidade, configuração, coleta, manutenção e avaliação [18].

Esses princípios sustentam a permanência do MQ-135 como indicador ou valor bruto até haver calibração defensável. Também sustentam a pendência do fator de conversão do pluviômetro e da definição das coordenadas e do sítio. Nenhuma fonte teórica valida fisicamente este protótipo.

### 4.4 Backend, banco e dashboard

HTTP fornece a semântica de métodos e respostas para uma API [15]. As restrições do PostgreSQL fundamentam `CHECK`, `NOT NULL`, `UNIQUE` e chaves estrangeiras no modelo relacional [16]. A WCAG 2.2 orienta requisitos de acessibilidade para conteúdo perceptível, operável, compreensível e robusto [7]. Essas fontes fundamentam decisões de software e critérios de avaliação; não provam conformidade da implementação futura.

A fundamentação completa, com as referências utilizadas e suas limitações, está em `docs/academico/n1/fundamentacao-teorica.md`.

## 5. Metodologia

O desenvolvimento utiliza sprints, tasks, branches, Pull Requests, critérios de aceite, matriz de rastreabilidade e Gates. Cada task deve registrar objetivo, responsável, dependências, artefatos, testes e limitações. Tasks independentes podem avançar em paralelo; uma dependência deve bloquear somente a parte que realmente precisa dela.

A metodologia classifica os resultados como **projetado**, **implementado**, **simulado**, **validado em software** ou **validado fisicamente**. A última classificação exige evidência de hardware ou bancada. A operação física não pode ser inferida de documentação, fixtures, código ou testes com doubles.

A integração ocorre pela `main` e depende de revisão centralizada. Commits têm título e descrição em português. Mudanças em arquitetura, contrato, schema, tecnologia ou fluxo de integração exigem avaliação arquitetural e ADR quando aplicável [6].

## 6. Requisitos

Os requisitos funcionais e não funcionais completos estão nos documentos de requisitos e na matriz [3] [4] [8]. A consolidação por grupo é a seguinte.

| Grupo | Conteúdo consolidado | Estado na N1 |
|---|---|---|
| RF-01 a RF-08 | Identificação da estação, aquisição das métricas, timestamp, qualidade e tratamento de leitura inválida | Contrato e validação de schema implementados; aquisição física e calibração pendentes |
| RF-09 a RF-13 | MQTT, reconexão, validação backend, persistência, healthcheck, consultas e resumo | Validação FastAPI implementada; MQTT, persistência runtime e consultas REST pendentes |
| RF-14 a RF-17 | Métricas atuais, histórico, localização e estados do dashboard | Projetados; frontend e coordenadas físicas pendentes |
| RF-18 a RF-23 | Displays, tempo, TCA9548A, isolamento de falhas e registro de falhas | Renderers, estados e tasks validados em software; integração física e observabilidade completa pendentes |
| RNF-01 a RNF-07 | Separação de camadas, ciclos independentes, operação degradada, stack, persistência, tempo e índice | Estrutura e modelo implementados; execução física e banco runtime pendentes |
| RNF-08 a RNF-15 | Separação do dashboard, acessibilidade, validação, segurança, logs, schema e testes | Validação documental e de software parcial; frontend, logs completos e camadas físicas pendentes |
| RNF-16 a RNF-20 | Governança Git, autoria, ADR, rastreabilidade e demonstração reproduzível | Aplicados documentalmente; demonstração física ainda pendente |

O contrato v1.0 exige `schema_version`, `station_id`, `timestamp`, `location`, `measurements` e `quality`. O tópico MQTT previsto é `estacao/<station_id>/telemetry`. O backend rejeita versões não suportadas, campos extras, timestamp inválido e identificador vazio nos testes complementares integrados à `main`.

## 7. Casos de uso

| Caso | Interação consolidada | Estado observável |
|---|---|---|
| UC-01 — Adquirir leitura ambiental | Firmware solicita leituras, associa métricas e timestamp e marca qualidade | Estrutura de serviço e falha parcial simuladas; sensores físicos bloqueados |
| UC-02 — Publicar telemetria | Firmware serializa e publica no tópico MQTT | Projetado; broker e publicação pendentes |
| UC-03 — Validar e ingerir telemetria | Backend recebe, valida, classifica e encaminha para persistência | Validação FastAPI em software; ingestão MQTT e persistência pendentes |
| UC-04 — Consultar estado e histórico | Dashboard consulta API, que acessa backend e banco | Endpoints de consulta e dashboard pendentes |
| UC-05 — Exibir meteorologia local | Estado externo e medição local são combinados e renderizados | Renderer testado com estado sintético; display e sensores físicos bloqueados |
| UC-06 — Manter relógio e calendário | NTP corrige e DS3231 sustenta referência local | Conversão temporal testada; NTP, RTC e OLED físicos bloqueados |
| UC-07 — Registrar falha e recuperar | Sistema registra falha e mantém funções independentes quando possível | Isolamento de driver testado; recuperação física e logs completos pendentes |
| UC-08 — Revisar entrega acadêmica | PO relaciona artefato, requisito, teste, evidência e limitação | Aplicado por branches, PRs, matriz e auditorias |

Os fluxos completos e os requisitos relacionados estão em `docs/requisitos/casos-de-uso.md` [5].

## 8. Arquitetura

A arquitetura separa aquisição, processamento, conectividade, apresentação, backend, persistência e dashboard. No firmware, modelos representam estados; serviços obtêm ou processam dados; tasks coordenam atualizações; displays renderizam estados recebidos. Os renderers não consultam diretamente sensores, API ou NTP.

O backend implementado contém `GET /health` e `POST /api/v1/telemetry/validate`. A implementação valida o payload e retorna HTTP 422 para entrada inválida. A própria aplicação informa que a validação não persiste dados e que a ingestão MQTT será adicionada posteriormente.

A arquitetura de produção prevê FastAPI, PostgreSQL, API REST e dashboard. Esses componentes estão na baseline, mas os endpoints de consulta, consumidor MQTT, conexão runtime com PostgreSQL e frontend ainda não são resultados disponíveis.

## 9. Modelagem de dados

O DER inicial contém `stations`, `measurements` e `measurement_quality`. Uma estação possui muitas medições. Cada medição referencia uma estação e possui instante medido, métricas ambientais e timestamp de criação. Cada registro de qualidade identifica uma métrica, seu estado e eventual motivo.

A migration define chaves primárias, chave estrangeira, unicidade do código da estação, estados de qualidade permitidos e índice `station_id + measured_at`. Os timestamps usam `TIMESTAMPTZ`, seguindo a política de armazenar UTC e converter na apresentação.

O modelo é projetado e implementado como artefato SQL versionado no repositório. Não há evidência de execução contra PostgreSQL nesta N1. Não há faixas físicas, calibração, coordenadas reais ou fator de conversão de chuva no modelo.

## 10. Protótipo e testes

O protótipo disponível é um skeleton de software e dados. Ele contém FastAPI, schema v1.0, fixtures válida/parcial/inválida, serviços e estados de firmware, renderizadores, tasks, DER, migration e validador de contrato.

A cobertura atual é:

| Camada | Resultado disponível | Classificação |
|---|---|---|
| Backend/API | 10 testes aprovados para healthcheck, payloads, campos extras, versão, timestamp e identificador | Validado em software |
| Firmware estrutural | 7 testes aprovados para drivers fake, renderizadores, tempo e tasks | Simulado e validado em software |
| Contrato | JSON, fixtures e regras v1.0 aprovados pelo validador e pelo CI | Validado em software |
| Banco | DER e migration presentes | Implementado como modelo; execução runtime pendente |
| Auditoria | Comparação entre arquitetura, contrato, requisitos, modelo e código | Validada por inspeção documental |
| Hardware | Nenhuma montagem, leitura ou calibração disponível | Bloqueado |

A auditoria técnica da Sprint 3 confirma que o contrato, os fixtures, a validação FastAPI e os serviços, estados e tasks de firmware possuem evidência de software. Ela também confirma que MQTT, PostgreSQL runtime, endpoints de consulta, dashboard, drivers concretos, pinagem, sensores, displays e testes de campo permanecem pendentes ou bloqueados [10].

Os testes planejados para MQTT, reconexão, persistência, NTP, DS3231, sensores, TCA9548A, calibração, dashboard, integração ponta a ponta e campo não são apresentados como executados.

## 11. Cronograma

O plano acadêmico organiza a N1 em cinco sprints e uma entrega final. A Sprint 1 consolidou especificação e baseline. A Sprint 2 consolidou projeto técnico, metodologia, fundamentação, cronograma e estrutura documental. A Sprint 3 consolidou evidências de software, auditoria, matriz e aderência disciplinar. A Sprint 4 consolida o relatório acadêmico. A Sprint 5 é destinada à auditoria e ao fechamento. A entrega está prevista para 02/10/2026 conforme o plano operacional [20].

O caminho crítico permanece:

```text
REQUISITOS → CONTRATO DE DADOS → FIRMWARE → INGESTÃO → BANCO → API → DASHBOARD → TESTES DE CAMPO → RESULTADOS/N2
```

A documentação e o software podem avançar sem hardware quando a atividade não depende de bancada. A ausência de hardware bloqueia somente as conclusões que exigem leitura real, pinagem, calibração, operação offline no dispositivo ou evidência física.

## 12. Resultados disponíveis

Os resultados desta N1 são exclusivamente os seguintes:

1. A especificação de requisitos, casos de uso, arquitetura, contrato e modelo de dados está versionada.
2. O backend FastAPI responde ao healthcheck e valida payloads conforme o schema v1.0.
3. Fixtures válida, parcial e inválida são exercitadas por testes.
4. Campos extras, versão não suportada e `station_id` vazio são rejeitados pelo modelo.
5. O firmware estrutural isola uma falha de driver e entrega estados aos renderizadores e tasks em testes com doubles.
6. O DER e a migration SQL representam o modelo inicial de estações, medições e qualidade.
7. O workflow de CI executa validação de contrato, testes backend, testes de firmware e compilação Python.
8. A documentação relaciona requisitos, implementação, testes, evidências, pendências e limitações.

Não há resultado disponível sobre exatidão de sensores, consumo, disponibilidade de rede, entrega MQTT, persistência PostgreSQL em execução, dashboard, autonomia, calibração, coordenadas, montagem ou teste de campo.

## 13. Análise dos resultados disponíveis

Os resultados demonstram coerência entre o contrato, o schema FastAPI, os fixtures e os testes de validação. A rejeição de campos extras e de versão não suportada reduz ambiguidades na fronteira de entrada. O tratamento de payload parcial demonstra que ausência de uma métrica não é convertida silenciosamente em zero.

Os testes de firmware demonstram separação de responsabilidades e comportamento estrutural com dependências simuladas. Eles não medem o comportamento elétrico, o tempo de ciclo, o consumo, a estabilidade ou a recuperação do ESP32 real.

O DER e a migration são coerentes com as entidades do contrato e com a necessidade de armazenar qualidade por métrica. Como o banco não foi executado nesta etapa, ainda não é possível concluir que consultas, transações, índices e constraints funcionem no ambiente PostgreSQL de destino.

A diferença entre o fluxo arquitetural previsto e o software implementado é uma lacuna de implementação, não uma alteração da arquitetura. O próximo avanço técnico deve priorizar ingestão MQTT, persistência runtime, endpoints de consulta e frontend, sem remover os bloqueios de hardware por suposição.

## 14. Conclusões e recomendações

A N1 consolidada apresenta uma especificação rastreável, arquitetura coerente, modelo de dados inicial, protótipo de software e testes automatizados aprovados. Esses resultados são suficientes para demonstrar a base documental e estrutural do produto.

A N1 não demonstra ainda a estação física. Não há autorização para declarar validação física de sensores, displays, pinagem, calibração, conectividade, operação offline ou medições ambientais. Essas conclusões dependem de evidências de bancada e de campo.

Recomenda-se que as próximas atividades mantenham a matriz atualizada e priorizem a implementação incremental das camadas ausentes. Cada avanço deve incluir teste, log ou evidência correspondente. A calibração do MQ-135, o fator do pluviômetro, as coordenadas, a pinagem e a infraestrutura do broker devem ser decididos e documentados antes de qualquer afirmação de conclusão.

## 15. Auditoria de coerência acadêmica

A auditoria também está registrada em `docs/academico/n1/auditoria-consolidacao-n1.md` para permitir revisão independente dos critérios abaixo.

A auditoria da consolidação, revisada após a integração de `docs/academico/n1/insumos-tecnicos-consolidacao.md`, verificou os seguintes pontos:

| Verificação | Resultado | Observação |
|---|---|---|
| Coerência entre contexto, objetivos e escopo | Aprovada | O objetivo de coleta, telemetria, persistência e visualização corresponde ao MVP e à arquitetura. |
| Coerência entre RF/RNF e arquitetura | Aprovada com pendências | Requisitos de hardware, MQTT, banco e dashboard estão identificados; implementação ausente não foi ocultada. |
| Referências e citações | Aprovada | A fundamentação possui referências numeradas e o relatório aponta para as fontes internas e externas. |
| Padrão acadêmico e ABNT aplicável | Parcialmente atendido | Há título, seções, citações numéricas, referências e indicação de apêndices. Elementos gráficos, capa e formatação final dependem do empacotamento acadêmico exigido. |
| Figuras e tabelas | Aprovada para a primeira versão | O relatório usa tabelas de síntese e diagramas textuais já versionados; não inventa imagens de hardware ou resultados gráficos. |
| Siglas | Aprovada | ESP32, MQTT, API, REST, NTP, RTC, OLED, DER, RF, RNF e MVP são explicadas no texto ou nos documentos de origem. |
| Separação entre resultados e análise | Aprovada | Resultados disponíveis e interpretação estão em seções distintas. |
| Afirmações sem evidência | Aprovada com ressalvas | As afirmações físicas e de desempenho são marcadas como projetadas, pendentes ou bloqueadas; a fundamentação teórica não é usada como validação do protótipo. |
| Validação física | Não disponível | Nenhum componente ou medição é declarado fisicamente validado. |

## 16. Apêndices indicados

A versão final pode incluir como apêndices o contrato JSON v1.0, fixtures de telemetria, matriz de rastreabilidade, casos de uso, DER, migration SQL, listagem dos testes, auditoria de coerência, cronograma e evidências de CI. Fotografias, logs de placa, leituras de referência e planilhas de campo somente devem ser adicionados quando existirem e estiverem vinculados a procedimentos reproduzíveis.

## Referências

[1]: ../../../docs/requisitos/contexto-escopo-objetivos.md "Contexto, problema, justificativa e objetivos"
[2]: ../../../docs/requisitos/stakeholders-e-escopo.md "Stakeholders, responsabilidades e fronteiras de escopo"
[3]: ../../../docs/requisitos/requisitos-funcionais.md "Requisitos funcionais"
[4]: ../../../docs/requisitos/requisitos-nao-funcionais.md "Requisitos não funcionais"
[5]: ../../../docs/requisitos/casos-de-uso.md "Casos de uso"
[6]: metodologia-desenvolvimento.md "Metodologia de desenvolvimento da N1"
[7]: fundamentacao-teorica.md "Fundamentação teórica"
[8]: ../../../docs/requisitos/matriz-rastreabilidade-n1.md "Matriz de rastreabilidade da N1"
[9]: prototipo-e-testes.md "Protótipo e casos de teste da N1"
[10]: ../../../docs/testes/auditoria-coerencia-s3.md "Auditoria de coerência técnica — Sprint 3"
[11]: https://www.iso.org/standard/69050.html "ISO 37122:2019 — Sustainable cities and communities: Indicators for smart cities"
[12]: https://documentation.espressif.com/esp32_datasheet_en.html "ESP32 Series Datasheet, Version 5.3"
[13]: https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html "MQTT Version 5.0"
[14]: https://www.w3.org/TR/WCAG22/ "Web Content Accessibility Guidelines (WCAG) 2.2"
[15]: https://www.rfc-editor.org/rfc/rfc9110 "RFC 9110 — HTTP Semantics"
[16]: https://www.postgresql.org/docs/current/ddl-constraints.html "PostgreSQL Documentation — Constraints"
[17]: https://standards.ieee.org/standard/29148-2018.html "IEEE/ISO/IEC 29148-2018 — Systems and software engineering — Life cycle processes — Requirements engineering"
[18]: https://www.epa.gov/air-sensor-toolbox/how-use-air-sensors-air-sensor-guidebook "How to Use Air Sensors: Air Sensor Guidebook / Enhanced Air Sensor Guidebook"
[19]: https://journals.sagepub.com/doi/10.1177/0309133320956567 "Low-cost electronic sensors for environmental research: Pitfalls and opportunities"
[20]: https://docs.google.com/document/d/1ij1nmvs1P_PxaeunHD-nefCdfW433h46/edit "Plano operacional N1 — Sprints James v2"
[21]: auditoria-consolidacao-n1.md "Auditoria de coerência da consolidação acadêmica da N1"
[22]: insumos-tecnicos-consolidacao.md "Insumos técnicos para consolidação da N1"
