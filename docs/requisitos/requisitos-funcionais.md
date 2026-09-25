# Requisitos funcionais

## 1. Objetivo

Este documento atende à task J-S1-03 da Sprint 1. Os requisitos funcionais descrevem comportamentos verificáveis do sistema. Cada requisito possui prioridade, origem e critério de aceite inicial. As faixas numéricas e decisões de hardware que ainda dependem de validação permanecem indicadas como pendências.

## 2. Convenções

- **P0:** obrigatório para o MVP ou para a demonstração da N1.
- **P1:** necessário para completar a integração ou melhorar a evidência, mas depende de insumos ainda não liberados.
- **TBD:** decisão ainda não confirmada.

## 3. Requisitos funcionais

| ID | Requisito | Prioridade | Critério de aceite inicial |
|---|---|---:|---|
| RF-01 | O sistema deve identificar a estação por um `station_id` configurável em cada amostra de telemetria. | P0 | Uma mensagem válida contém `station_id` e o backend não associa silenciosamente uma estação desconhecida. |
| RF-02 | O firmware deve adquirir temperatura e umidade pelos sensores definidos para a configuração aprovada. | P0 | A amostra contém temperatura e umidade ou informa erro de leitura sem inventar valores. |
| RF-03 | O firmware deve adquirir pressão atmosférica. | P0 | A amostra contém pressão ou informa erro de leitura com seu estado de qualidade. |
| RF-04 | O sistema deve adquirir um indicador de qualidade do ar por meio do subsistema aprovado. | P0 | A amostra registra o valor bruto e seu estado de qualidade; conversão para concentração só ocorre após calibração aprovada. |
| RF-05 | O sistema deve adquirir luminosidade como medida relativa ou unidade definida em documentação aprovada. | P0 | A unidade e o método de conversão estão documentados antes da apresentação do valor. |
| RF-06 | O sistema deve adquirir precipitação/pluviometria e registrar o resultado conforme o modelo do pluviômetro validado. | P0 | O cálculo de `rain_mm` somente é considerado concluído após definição do equipamento e do fator de conversão. |
| RF-07 | O firmware deve registrar timestamp e identificação da estação em cada amostra. | P0 | A amostra possui timestamp em formato ISO-8601 e `station_id`; timestamp inválido é rejeitado pelo backend. |
| RF-08 | O firmware deve validar leituras antes da transmissão e marcar a qualidade de cada métrica. | P0 | Falhas, valores suspeitos ou inválidos são identificados sem substituição silenciosa por zero. |
| RF-09 | O firmware deve transmitir telemetria por Wi-Fi usando MQTT como caminho principal. | P0 | Uma mensagem válida é publicada em `estacao/<station_id>/telemetry` quando a conectividade está disponível. |
| RF-10 | O firmware deve realizar tentativas controladas de reconexão Wi-Fi e MQTT sem bloquear indefinidamente as demais funções. | P0 | A perda de conectividade não congela a aquisição ou as telas; as tentativas ficam registradas. |
| RF-11 | O backend deve validar novamente schema, versão, timestamp, estação e integridade da telemetria recebida. | P0 | Payload incompatível é rejeitado ou colocado em quarentena conforme regra documentada, com log da causa. |
| RF-12 | O backend deve persistir medições válidas e a qualidade das métricas no banco relacional. | P0 | Uma medição persistida pode ser relacionada à estação, ao instante e aos estados de qualidade. |
| RF-13 | A API REST deve expor saúde da aplicação, estações, última leitura, histórico e resumo. | P0 | Os endpoints baseline são documentados e retornam respostas coerentes com o banco. |
| RF-14 | O dashboard deve apresentar os valores atuais das métricas previstas no MVP. | P0 | O usuário visualiza temperatura, umidade, pressão, qualidade do ar, luminosidade e chuva quando houver dados disponíveis. |
| RF-15 | O dashboard deve permitir consulta de histórico por período. | P0 | O usuário consegue selecionar ou informar um período e visualizar os dados retornados pela API. |
| RF-16 | O dashboard deve representar a localização da estação quando as coordenadas forem definidas. | P0 | A localização exibida corresponde às coordenadas aprovadas e não a valores inventados. |
| RF-17 | O dashboard deve exibir estados de carregamento, erro e ausência de dados. | P0 | Falhas e dados ausentes são comunicados de modo compreensível, sem usar zero como substituto silencioso. |
| RF-18 | O display meteorológico deve apresentar estado processado que combine dados externos aprovados e medições locais do BME280. | P1 | O renderer recebe estado preparado e não consulta diretamente sensores ou API. |
| RF-19 | O display de relógio/calendário deve apresentar hora, data e dia da semana. | P1 | A interface exibe hora, minutos, dia, mês, ano e dia da semana a partir do serviço de tempo. |
| RF-20 | O serviço de tempo deve usar NTP para correção periódica e DS3231 como referência local durante a indisponibilidade de internet. | P1 | O fluxo online/offline e a correção do RTC são documentados e testados. |
| RF-21 | O sistema deve controlar os dois displays pelo TCA9548A em canais independentes. | P1 | O canal 0 corresponde ao display meteorológico e o canal 1 ao display de relógio/calendário. |
| RF-22 | Uma falha em sensor, display, API meteorológica ou TCA9548A não deve derrubar desnecessariamente as demais funções. | P0 | O componente afetado registra falha e as funções independentes continuam operando quando possível. |
| RF-23 | O sistema deve registrar falhas relevantes de sensor, conectividade, publicação, ingestão e dependências críticas. | P0 | Os logs permitem identificar o tipo de falha sem expor credenciais. |

## 4. Contratos relacionados

O payload baseline deve conter `schema_version`, `station_id`, `timestamp`, `location`, `measurements` e `quality`. A versão inicial é `1.0`. Alterações incompatíveis exigem avaliação arquitetural e estratégia de compatibilidade.

## 5. Pendências que afetam aceite

Os seguintes critérios não podem ser considerados fechados sem validação adicional: pinagem dos sensores, modelo e conversão do pluviômetro, calibração do MQ-135, faixas numéricas de validação, coordenadas da estação e infraestrutura final do broker. Enquanto não houver decisão aprovada, esses itens devem permanecer como TBD na documentação e nos testes.

## 6. Referências

[1]: ../arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
