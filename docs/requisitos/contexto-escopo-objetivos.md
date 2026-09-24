# Contexto, problema, justificativa e objetivos

## 1. Identificação

Este documento registra o contexto e os limites iniciais do projeto **Estação Meteorológica Inteligente com ESP32**. Ele atende à task J-S1-01 da Sprint 1 e serve como base para os requisitos, casos de uso e critérios de aceite.

O projeto está inserido na disciplina **Ciência da Computação — Projeto e Desenvolvimento II (68F3)**. A solução deve integrar sistemas embarcados, comunicação, backend, banco de dados, dashboard web e documentação acadêmica.

## 2. Contexto

O projeto propõe uma estação meteorológica urbana capaz de coletar dados ambientais, transmiti-los, armazená-los e disponibilizá-los para consulta pública. O sistema combina um dispositivo embarcado baseado em ESP32 com sensores ambientais, um pipeline de telemetria e uma aplicação web para visualização.

A arquitetura baseline define o seguinte fluxo:

```text
Sensores → ESP32/MicroPython → Wi-Fi → MQTT → Backend Python → PostgreSQL → API REST → Dashboard Web
```

O dispositivo também possui duas interfaces locais. A primeira apresenta informações meteorológicas externas e medições locais do BME280. A segunda apresenta data e hora, usando NTP para correção periódica e DS3231 como referência local durante a indisponibilidade de internet. Essas telas complementam o dashboard web e não o substituem.

## 3. Problema

O projeto precisa demonstrar, de forma integrada e academicamente rastreável, como uma leitura ambiental pode sair de sensores conectados ao ESP32, ser validada e transmitida, chegar ao backend, ser persistida e ser apresentada ao usuário. Sem uma especificação comum, as frentes de hardware, firmware, backend, banco, frontend e documentação podem produzir artefatos incompatíveis ou evidências que não comprovem os objetivos do projeto.

O problema de engenharia e documentação é, portanto, estabelecer um escopo verificável, contratos claros e uma cadeia de evidências que permita demonstrar o funcionamento do sistema sem ocultar limitações, pendências ou diferenças entre simulação e operação física.

## 4. Justificativa

A solução é relevante para o contexto acadêmico porque integra aquisição de dados, sistemas embarcados, comunicação IoT, persistência, visualização, validação e engenharia de software em um único produto demonstrável. A organização por requisitos e critérios de aceite permite relacionar cada decisão técnica a testes e evidências para as entregas N1 e N2.

A abordagem também reduz o risco de apresentar como concluído um comportamento que ainda depende de validação física. Questões como pinagem, calibração do MQ-135, fator de conversão do pluviômetro, coordenadas da estação e infraestrutura final de broker permanecem explícitas como pendências até que existam dados ou decisões aprovadas.

## 5. Objetivo geral

Projetar e validar uma estação meteorológica urbana baseada em ESP32 que colete dados ambientais, transmita telemetria, persista histórico e disponibilize informações por API REST e dashboard web público, com documentação e evidências coerentes com os requisitos acadêmicos.

## 6. Objetivos específicos

1. Definir requisitos funcionais, não funcionais, stakeholders, casos de uso e critérios de aceite.
2. Integrar sensores ambientais ao ESP32 respeitando as limitações elétricas e de comunicação dos componentes.
3. Implementar aquisição periódica, validação, tratamento de falhas e transmissão por Wi-Fi e MQTT.
4. Definir e preservar um contrato de telemetria versionado entre firmware e backend.
5. Implementar ingestão, validação, persistência e consulta de dados no backend Python.
6. Modelar o armazenamento histórico em banco relacional.
7. Disponibilizar dados atuais, históricos e agregações por API REST.
8. Desenvolver dashboard web responsivo, acessível e separado do banco de dados.
9. Implementar e validar as duas telas OLED locais, incluindo operação degradada e referência temporal pelo DS3231.
10. Registrar testes, evidências, limitações e resultados de modo reproduzível para N1 e N2.

## 7. Escopo do MVP

O MVP deve coletar temperatura, umidade, pressão atmosférica, indicador de qualidade do ar, luminosidade e precipitação. Cada amostra deve conter identificação da estação e timestamp. Leituras devem ser validadas no firmware e no backend, e falhas relevantes devem ser registradas.

O MVP também deve persistir dados históricos, expor o último estado e o histórico por API, apresentar informações atuais e históricas em dashboard público e representar a localização da estação quando as coordenadas estiverem definidas.

## 8. Fora do MVP

Não fazem parte do MVP obrigatório: previsão meteorológica por aprendizado de máquina, rede mesh com múltiplas estações, aplicativo mobile nativo, painel solar e bateria como requisito obrigatório, caixa IP65 definitiva e alertas multicanal de produção. Esses itens podem ser registrados como trabalhos futuros, mas não devem consumir esforço que coloque N1 ou N2 em risco.

## 9. Limites e pendências

As seguintes decisões permanecem pendentes e não devem ser resolvidas por suposição:

- pinagem definitiva do ESP32;
- modelo exato do pluviômetro e fator de conversão para milímetros;
- procedimento de calibração e interpretação do MQ-135;
- infraestrutura final de hospedagem e broker;
- coordenadas físicas da estação;
- faixas finais de validação baseadas em datasheets e testes;
- datas e critérios adicionais de N1 e N2 eventualmente fornecidos pelo professor;
- simplificação ou coexistência final entre sensores com funções sobrepostas.

## 10. Referências

[1]: ../arquitetura/arquitetura-sistema.md "Arquitetura do Projeto — Estação Meteorológica Inteligente"
