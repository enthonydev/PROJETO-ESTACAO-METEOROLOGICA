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
| RF-02 | O firmware deve adquirir temperatura e umidade pelo DHT22 da configuração aprovada. | P0 | A amostra contém temperatura e umidade ou informa erro de leitura sem inventar valores. |
| RF-03 | O firmware deve adquirir pressão atmosférica pelo BMP280 da configuração aprovada. | P0 | A amostra contém pressão ou informa erro de leitura com seu estado de qualidade. |
| RF-04 | O sistema deve adquirir uma leitura bruta/experimental do MQ-135 como indicador de qualidade do ar. | P0 | A amostra registra o valor bruto e seu estado de qualidade; não se declara ppm sem calibração aprovada. |
| RF-05 | O sistema deve adquirir luminosidade relativa pelo LDR. | P0 | A leitura é apresentada como relativa; lux somente pode ser usado após calibração e documentação aprovadas. |
| RF-06 | O sistema deve adquirir a resposta do módulo de chuva como detecção/avaliação experimental. | P0 | `rain_mm` permanece ausente ou inválido até existir método e fator de conversão validados. |
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
| RF-18 | A única OLED I²C deve apresentar um estado local composto, com medições locais, data/hora e informação externa complementar quando disponível. | P1 | O renderer recebe estado preparado e não consulta diretamente sensores ou API. |
| RF-19 | O serviço de tempo deve fornecer data e hora para a OLED local. | P1 | A interface exibe a referência temporal disponível a partir do serviço de tempo. |
| RF-20 | O serviço de tempo deve usar NTP como fonte principal de sincronização. | P1 | A ausência de NTP é sinalizada; sem RTC dedicado, não se promete horário correto durante períodos offline prolongados. |
| RF-21 | O sistema deve controlar uma única OLED I²C 128x64, sem TCA9548A. | P1 | O estado local composto é entregue à única interface local aprovada. |
| RF-22 | Uma falha em sensor, OLED, API meteorológica ou conectividade não deve derrubar desnecessariamente aquisição e telemetria. | P0 | O componente afetado registra falha e as funções independentes continuam operando quando possível. |
| RF-23 | O sistema deve registrar falhas relevantes de sensor, conectividade, publicação, ingestão e dependências críticas. | P0 | Os logs permitem identificar o tipo de falha sem expor credenciais. |

## 4. Contratos relacionados

O payload baseline deve conter `schema_version`, `station_id`, `timestamp`, `location`, `measurements` e `quality`. A versão inicial é `1.0`. Alterações incompatíveis exigem avaliação arquitetural e estratégia de compatibilidade.

## 5. Pendências que afetam aceite

Os seguintes critérios não podem ser considerados fechados sem validação adicional: pinagem dos sensores, modelo e conversão do pluviômetro, calibração do MQ-135, faixas numéricas de validação, coordenadas da estação e infraestrutura final do broker. Enquanto não houver decisão aprovada, esses itens devem permanecer como TBD na documentação e nos testes.

## 6. Referências

[1]: ../arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
[2]: ../arquitetura/adr/ADR-002-adequacao-arquitetura-fisica-orcamento.md "ADR-002 — Adequação da arquitetura física por restrição orçamentária"
