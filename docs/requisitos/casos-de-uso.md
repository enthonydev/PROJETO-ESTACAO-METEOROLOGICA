# Casos de uso

## 1. Objetivo

Este documento atende à task J-S1-05 da Sprint 1. Os casos de uso representam as interações principais entre atores e o sistema e servem de ponte entre escopo, requisitos, testes e evidências.

Os fluxos abaixo descrevem o comportamento esperado da baseline. Detalhes de pinagem, calibração, infraestrutura e regras de faixa permanecem condicionados às decisões pendentes registradas nos requisitos.

## 2. Atores

- **Firmware da estação:** executa aquisição, validação, controle temporal, conectividade e publicação.
- **Sensor ambiental:** fornece leitura de uma métrica física.
- **Broker MQTT:** transporta a telemetria entre a estação e o backend.
- **Backend:** valida, processa e persiste telemetria.
- **Banco de dados:** armazena estações, medições e qualidade.
- **Usuário público:** consulta o dashboard.
- **API meteorológica externa:** fornece dados complementares para o display meteorológico.
- **Serviço NTP:** fornece referência externa para correção temporal.
- **RTC DS3231:** fornece referência temporal local durante indisponibilidade de internet.
- **Responsável técnico/PO:** revisa artefatos, critérios, evidências e decisões de escopo.

## 3. UC-01 — Adquirir leitura ambiental

**Objetivo:** produzir uma amostra com as leituras disponíveis dos sensores.

**Atores principais:** Firmware da estação, sensor ambiental.

**Pré-condições:** ESP32 inicializado e sensor configurado conforme a validação física disponível.

**Fluxo principal:**

1. O firmware inicia o ciclo periódico de aquisição.
2. O firmware solicita as leituras de temperatura, umidade, pressão, qualidade do ar, luminosidade e precipitação.
3. Cada leitura é associada à sua métrica e ao instante de aquisição.
4. O firmware marca a qualidade de cada métrica.
5. O firmware produz o estado da amostra para validação e serialização.

**Fluxos alternativos:**

- Se um sensor falhar, a métrica recebe estado de erro e as demais leituras continuam quando possível.
- Se a faixa final ainda não tiver sido aprovada, o valor não é classificado por uma faixa inventada; a pendência permanece documentada.

**Pós-condições:** Existe uma amostra parcial ou completa, com estados de qualidade explícitos.

**Requisitos relacionados:** RF-01, RF-02, RF-03, RF-04, RF-05, RF-06, RF-07, RF-08, RF-22.

## 4. UC-02 — Publicar telemetria

**Objetivo:** transmitir uma amostra validada ao backend pelo caminho principal.

**Atores principais:** Firmware da estação, Broker MQTT.

**Pré-condições:** Existe uma amostra serializável e a conectividade Wi-Fi/MQTT está disponível ou em processo controlado de reconexão.

**Fluxo principal:**

1. O firmware serializa a amostra conforme o schema de telemetria vigente.
2. O firmware publica a mensagem em `estacao/<station_id>/telemetry`.
3. O firmware registra o resultado da publicação sem expor credenciais.

**Fluxos alternativos:**

- Se o Wi-Fi estiver indisponível, o firmware inicia tentativas controladas sem bloquear a aquisição e as telas.
- Se o broker estiver indisponível, o firmware registra a falha e tenta reconectar conforme a política aprovada.

**Pós-condições:** A publicação é confirmada ou a falha é registrada para diagnóstico.

**Requisitos relacionados:** RF-07, RF-09, RF-10, RF-23, RNF-13.

## 5. UC-03 — Validar e ingerir telemetria

**Objetivo:** receber telemetria, validar sua integridade e encaminhar dados válidos para persistência.

**Atores principais:** Broker MQTT, Backend.

**Pré-condições:** Backend em execução e consumidor MQTT configurado.

**Fluxo principal:**

1. O backend recebe a mensagem do tópico esperado.
2. O backend valida a versão do schema, o `station_id`, o timestamp, a estrutura e os valores recebidos.
3. O backend registra a qualidade e os motivos de valores inválidos ou suspeitos.
4. O backend encaminha a medição válida para persistência.
5. O backend registra o resultado da ingestão.

**Fluxos alternativos:**

- Payload incompatível é rejeitado ou colocado em quarentena conforme regra documentada.
- Estação desconhecida não é associada silenciosamente.
- Falha parcial é persistida somente quando o modelo aprovado permitir, mantendo a qualidade das métricas inválidas.

**Pós-condições:** A mensagem é persistida, rejeitada ou colocada em quarentena com motivo rastreável.

**Requisitos relacionados:** RF-01, RF-07, RF-08, RF-11, RF-12, RF-23, RNF-06, RNF-10, RNF-13.

## 6. UC-04 — Consultar estado atual e histórico

**Objetivo:** disponibilizar dados persistidos para o dashboard.

**Atores principais:** Usuário público, API REST, Backend, Banco de dados.

**Pré-condições:** API disponível e dados consultáveis para a estação solicitada.

**Fluxo principal:**

1. O usuário acessa o dashboard.
2. O dashboard solicita a lista de estações ou uma estação específica.
3. A API consulta a última leitura, o histórico ou o resumo solicitado.
4. O backend retorna os dados e seus estados de qualidade.
5. O dashboard apresenta o resultado.

**Fluxos alternativos:**

- Se não houver dados, o dashboard apresenta ausência de dados.
- Se a API ou uma dependência falhar, o dashboard apresenta estado de erro compreensível.
- O frontend não acessa o PostgreSQL diretamente.

**Pós-condições:** O usuário vê os dados disponíveis ou uma mensagem explícita sobre erro ou ausência de dados.

**Requisitos relacionados:** RF-13, RF-14, RF-15, RF-16, RF-17, RNF-08, RNF-09.

## 7. UC-05 — Exibir meteorologia local

**Objetivo:** mostrar no OLED meteorológico o estado processado pela estação.

**Atores principais:** Firmware da estação, Display meteorológico, API meteorológica externa, BME280.

**Pré-condições:** Display, TCA9548A e fontes de dados disponíveis conforme o ambiente de execução.

**Fluxo principal:**

1. O serviço de sensores atualiza as medições locais do BME280.
2. O serviço meteorológico consulta a API externa em periodicidade própria.
3. O firmware combina os dados aprovados em um estado de apresentação.
4. O firmware seleciona o canal 0 do TCA9548A.
5. O renderer exibe o estado no OLED meteorológico.

**Fluxos alternativos:**

- Se a API externa falhar, o estado externo válido anterior é mantido e pode ser marcado como desatualizado.
- Se a internet falhar, as medições locais continuam sendo exibidas quando o BME280 estiver disponível.
- O renderer não consulta diretamente API ou sensor.

**Pós-condições:** A tela exibe o estado disponível sem interromper telemetria ou a outra tela.

**Requisitos relacionados:** RF-18, RF-22, RNF-01, RNF-02, RNF-03.

## 8. UC-06 — Manter relógio e calendário

**Objetivo:** manter e exibir data e hora mesmo durante indisponibilidade de internet.

**Atores principais:** Firmware da estação, Serviço NTP, RTC DS3231, Display de relógio.

**Pré-condições:** DS3231 e display configurados; NTP disponível apenas quando houver internet.

**Fluxo principal:**

1. O serviço de tempo lê a referência local do DS3231.
2. Quando houver conexão, o serviço consulta NTP em periodicidade controlada.
3. Após sincronização válida, o serviço pode corrigir o RTC.
4. O serviço entrega hora, data e dia da semana ao renderer.
5. O firmware seleciona o canal 1 do TCA9548A.
6. O renderer exibe o calendário e o relógio.

**Fluxos alternativos:**

- Sem internet, o DS3231 sustenta a referência local.
- Se a sincronização NTP falhar, o relógio continua com a referência local e a falha é registrada.
- O renderer não executa NTP diretamente.

**Pós-condições:** A tela de relógio continua operando de forma independente da API meteorológica.

**Requisitos relacionados:** RF-19, RF-20, RF-21, RF-22, RNF-02, RNF-03.

## 9. UC-07 — Registrar falha e recuperar operação

**Objetivo:** permitir diagnóstico e continuidade após uma falha parcial.

**Atores principais:** Firmware da estação, Backend, Responsável técnico/PO.

**Pré-condições:** Um sensor, display, rede, broker, API, banco ou dependência temporal apresenta falha.

**Fluxo principal:**

1. O componente detecta a falha.
2. O sistema registra tipo, contexto e impacto sem expor segredos.
3. As funções independentes continuam quando possível.
4. O sistema realiza tentativa de recuperação conforme a política aprovada.
5. O sistema registra o retorno à operação.
6. A equipe associa logs e resultados aos casos de teste e às evidências.

**Pós-condições:** A falha e a recuperação, quando ocorrerem, ficam rastreáveis.

**Requisitos relacionados:** RF-10, RF-22, RF-23, RNF-03, RNF-12, RNF-14, RNF-15.

## 10. UC-08 — Revisar entrega acadêmica

**Objetivo:** verificar se uma task está pronta para integração e uso como evidência acadêmica.

**Atores principais:** James, Enthony, Luan e professor da disciplina, conforme a etapa de revisão.

**Pré-condições:** Artefato produzido, testes executados quando aplicável e pendências identificadas.

**Fluxo principal:**

1. O responsável apresenta o artefato e seu vínculo com os requisitos.
2. São apresentados testes, evidências, limitações e dependências.
3. O PO revisa escopo, arquitetura e critérios de aceite.
4. Pendências são classificadas como bloqueadoras ou não bloqueadoras.
5. A revisão é registrada antes da conclusão da task ou abertura/atualização do PR.

**Pós-condições:** O artefato é aprovado, devolvido para correção ou explicitamente mantido como pendente.

**Requisitos relacionados:** RNF-14, RNF-15, RNF-16, RNF-18, RNF-19, RNF-20.

## 11. Matriz resumida de rastreabilidade

| Caso de uso | Requisitos principais | Evidência esperada |
|---|---|---|
| UC-01 | RF-01 a RF-08, RF-22 | Caso de teste de aquisição e falha parcial; simulação ou bancada identificada |
| UC-02 | RF-07, RF-09, RF-10, RF-23 | Fixture/payload, log de publicação e teste de reconexão |
| UC-03 | RF-01, RF-07, RF-08, RF-11, RF-12, RF-23 | Testes de schema, estação desconhecida, timestamp e persistência |
| UC-04 | RF-13 a RF-17 | Testes de API e screenshots/evidências do dashboard, quando implementado |
| UC-05 | RF-18, RF-22, RNF-01 a RNF-03 | Teste online/offline e evidência dos dois estados |
| UC-06 | RF-19 a RF-21, RNF-02, RNF-03 | Teste NTP/RTC, indisponibilidade de internet e evidência do display |
| UC-07 | RF-10, RF-22, RF-23, RNF-03, RNF-12 a RNF-15 | Logs, casos de recuperação e relatório de falha |
| UC-08 | RNF-14 a RNF-20 | Registro de revisão, checklist e relatório de Gate |

## 12. Referências

[1]: ../arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
