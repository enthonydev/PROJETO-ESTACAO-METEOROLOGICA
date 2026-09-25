# Fundamentação teórica

## 1. Objetivo e delimitação

Este documento atende à task J-S2-03 da Sprint 2. A fundamentação relaciona o produto aos conceitos de cidades inteligentes, Internet das Coisas, sistemas embarcados, telemetria, medições ambientais, backend, visualização web, geolocalização e engenharia de software.

As fontes sustentam conceitos, decisões de projeto e métodos de avaliação. Elas **não validam fisicamente** a Estação Meteorológica Inteligente deste projeto. Exatidão, estabilidade, incerteza, representatividade, disponibilidade, segurança e conformidade devem ser demonstradas por ensaios, testes e evidências próprias.

## 2. Cidades inteligentes e monitoramento ambiental

Cidades inteligentes utilizam dados e tecnologias de informação para apoiar serviços e decisões urbanas. Uma revisão sistemática sobre sensores em sistemas IoT para o desenvolvimento sustentável de cidades inteligentes identifica aplicações ambientais relacionadas a qualidade do ar, ruído urbano e solo, além de discutir sensores, comunicação e análise de dados como partes de sistemas integrados [1]. Outra revisão relaciona IoT, sensores e monitoramento ambiental a aplicações como qualidade do ar, poluição da água e agricultura, mas também registra desafios de interoperabilidade entre sensores heterogêneos, ruído, amostras limitadas e infraestrutura de rede [2].

Esses estudos justificam o problema do projeto: uma estação com aquisição, transmissão, persistência e visualização pode produzir uma fonte estruturada de dados ambientais urbanos. A justificativa não elimina os requisitos de qualidade. Dados coletados por sensores precisam de metadados, tratamento de falhas, controle de qualidade e uma interpretação compatível com o propósito da medição.

A ISO 37122:2019 fornece indicadores e metodologias para mensurar cidades inteligentes [3]. No projeto, essa referência deve ser usada para fundamentar a importância de indicadores e da mensuração urbana. Ela não deve ser apresentada como especificação de hardware, norma de calibração dos sensores ou certificação da estação.

## 3. ESP32 e MicroPython em sistemas embarcados

A ficha técnica do ESP32 descreve um sistema em chip com Wi-Fi de 2,4 GHz, Bluetooth, memória, GPIO, ADC, DAC, I2C, SPI, UART, temporizadores, watchdog e modos de baixo consumo [4]. Esses recursos são compatíveis, em nível de capacidade, com uma estação que precisa adquirir sinais, controlar periféricos e transmitir dados.

A documentação do MicroPython para ESP32 apresenta APIs para GPIO, ADC, I2C, SPI, UART, WLAN, temporização e modos de suspensão [5]. Ela também registra restrições que precisam ser consideradas no projeto elétrico: ADC2 pode conflitar com Wi-Fi, GPIO34–39 são somente de entrada e alguns pinos possuem funções reservadas. Essas informações orientam a validação da pinagem, mas não autorizam a escolha de GPIOs sem conferência com a placa, os sensores e a alimentação reais.

Um estudo comparativo de C/C++, MicroPython, Rust e TinyGo em cinco algoritmos embarcados encontrou tempos de execução maiores para MicroPython, embora reconheça a vantagem de desenvolvimento mais simples e rápido para aplicações de nível mais alto [6]. Esse resultado sustenta o uso de MicroPython para prototipagem, aquisição periódica, controle e comunicação, mas não demonstra desempenho da estação concreta. O tempo de ciclo, o consumo, a estabilidade e a capacidade de recuperação devem ser verificados na implementação escolhida.

## 4. IoT e MQTT para telemetria

A especificação MQTT 5.0 define um protocolo de transporte de mensagens baseado em publicação e assinatura, adequado também a ambientes restritos de IoT [7]. O desacoplamento entre publicadores e assinantes permite separar a estação física do backend. Essa propriedade é compatível com o fluxo do projeto:

```text
Sensores → ESP32/MicroPython → Wi-Fi → MQTT → Backend → PostgreSQL → API REST → Dashboard
```

A mesma especificação distingue níveis de qualidade de serviço. QoS 0 entrega uma mensagem no máximo uma vez e admite perda. QoS 1 busca entrega pelo menos uma vez e pode gerar duplicatas. QoS 2 busca entrega exatamente uma vez, com maior complexidade e overhead [7]. Por isso, a escolha do QoS não substitui decisões sobre `station_id`, timestamp, identificação de mensagem, persistência, retransmissão, deduplicação e observabilidade.

Um estudo aplicado descreve uma estação de baixo custo baseada em ESP32, sensores ambientais, broker MQTT e aplicações web e móveis [8]. O trabalho é um precedente de arquitetura e de integração. Seus testes foram realizados em uma implementação e local específicos, durante período delimitado, portanto não constituem validação da estação deste projeto.

## 5. Medições ambientais e qualidade dos dados

A qualidade de uma medição depende do conjunto sensor, instalação, aquisição, calibração, controle de qualidade e contexto de uso. A orientação da WMO/ISO sobre classificação de sítios informa que a localização de um instrumento afeta a representatividade dos dados e que a classificação serve como indicação para os usuários, não como garantia geral de qualidade [9]. O propósito da estação, a exposição, o entorno e os metadados precisam ser documentados.

A EPA recomenda que estudos com sensores definam pergunta, plano, objetivos de qualidade, configuração, coleta, avaliação, manutenção e comunicação dos dados [10]. O guia também enfatiza verificações, completude, outliers, deriva, manutenção preventiva e comparação ou colocalização com referência quando aplicável. O guia é específico para sensores de qualidade do ar; neste projeto, seus princípios são usados como referência metodológica e não como critério meteorológico automático.

A literatura sobre sensores eletrônicos de baixo custo descreve riscos de deriva, interferência ambiental, degradação, falhas de montagem e diferenças entre laboratório e condições finais de implantação [11]. O trabalho recomenda calibração nas condições de uso, avaliação contínua e calibração cruzada com instrumentos de referência quando aplicável.

Um estudo de qualidade de dados meteorológicos de baixo custo comparou medições com uma estação de referência e utilizou correlação, erros e análise dos resíduos [12]. O artigo relata resultados específicos para o sistema, local e período estudados. Esses números não podem ser copiados para o protótipo. Eles apenas justificam a necessidade de comparar, por variável, as leituras da estação com uma referência e registrar métricas, período, condições e limitações.

Essas fontes sustentam três decisões do projeto. O MQ-135 deve permanecer como indicador ou valor bruto enquanto não houver calibração tecnicamente defensável. O pluviômetro precisa de modelo e fator de conversão documentados. As coordenadas e a instalação da estação precisam ser definidas e registradas antes de qualquer afirmação sobre representatividade espacial.

## 6. Backend, API e persistência

HTTP define a semântica de métodos, conteúdos e códigos de resposta que sustentam a exposição de recursos por uma API [13]. No projeto, essa referência apoia a separação entre ingestão de telemetria e consulta pelo dashboard. Ela não define sozinha autenticação, autorização, schema JSON, observabilidade ou segurança operacional; essas decisões precisam ser especificadas no próprio sistema.

A PEP 249 define uma interface comum de acesso a bancos de dados em Python, incluindo conexões, cursores, confirmação, reversão e exceções [14]. Essa abstração ajuda a organizar o acesso a dados sem misturar regras de negócio com detalhes de persistência.

A documentação do PostgreSQL descreve restrições como `CHECK`, `NOT NULL`, `UNIQUE` e chaves estrangeiras para limitar valores e relações no banco [15]. Essas restrições fundamentam o modelo de estações, medições e qualidade das medições. No projeto, a migration deve manter a relação entre estação e medição, impedir métricas de qualidade desconhecidas e preservar o índice de série temporal definido na baseline.

Um artigo sobre uma arquitetura de software de estação meteorológica em tempo real descreve uma solução modular, com polling de data loggers, conectores configuráveis e implementação em Python [16]. O caso apoia a separação de responsabilidades e a possibilidade de testar software antes da integração completa. Ele não demonstra a qualidade dos sensores ou a validade da infraestrutura do projeto atual.

## 7. Dashboard, acessibilidade e geolocalização

Um dashboard é a camada que transforma respostas da API em informação interpretável. Estudos de sistemas de monitoramento meteorológico e agrícola descrevem o uso de dashboards web para comunicar dados de sensores, análises e alertas [17]. No projeto, essa camada deve permanecer desacoplada do banco e apresentar dados atuais, históricos, localização e estados de carregamento, erro e ausência de dados.

A WCAG 2.2 organiza acessibilidade em quatro princípios: perceptível, operável, compreensível e robusto [18]. A diretriz exige critérios testáveis e oferece orientação para alternativas textuais, contraste, teclado, foco e mensagens de status. Um gráfico meteorológico não deve depender somente de cor ou forma; deve ter alternativa textual ou dados acessíveis. Seguir a WCAG orienta o desenvolvimento, mas não prova conformidade sem avaliação da implementação, tecnologias assistivas e, idealmente, testes com usuários.

A especificação de Geolocation do W3C exige permissão do usuário para obter a localização do dispositivo e trata a informação como sensível [19]. Ela também alerta que a posição obtida não é necessariamente a localização real do dispositivo e recomenda finalidade definida, minimização, proteção e transparência. Como a estação possui localização fixa, o dashboard não deve substituir suas coordenadas cadastradas pela geolocalização do navegador do usuário. Se a geolocalização do usuário for necessária para uma função futura, ela deverá possuir finalidade, consentimento e tratamento de erro documentados.

## 8. Engenharia de requisitos, testes e rastreabilidade

A ISO/IEC/IEEE 12207:2017 fornece processos de ciclo de vida para sistemas de software [20]. A página oficial da ISO informa que essa edição está em retirada; portanto, ela é uma referência de processo neste documento, e a edição vigente deve ser confirmada antes de qualquer declaração de conformidade normativa.

A ISO/IEC/IEEE 29148:2018 trata de processos e produtos de engenharia de requisitos ao longo do ciclo de vida e fornece atributos e características de requisitos [21]. A ISO/IEC/IEEE 29119-1:2022 fornece conceitos gerais para testes de software [22]. Essas referências sustentam a separação entre requisitos, critérios de aceite, casos de teste, resultados e evidências.

Um estudo de rastreabilidade de medições meteorológicas descreve uma cadeia com aquisição, armazenamento, calibração por padrões e orçamento de incerteza em um contexto metrológico específico [23]. O caso demonstra que software e procedimentos de calibração participam da qualidade do arquivo de medições. Ele não valida a estação deste projeto, mas ajuda a definir o tipo de evidência que será necessário produzir quando houver hardware e instrumentos de referência disponíveis.

A matriz `docs/requisitos/matriz-rastreabilidade-n1.md` aplica esses princípios ao projeto. Cada requisito deve ser relacionado ao artefato que o implementa, ao caso de teste correspondente e à evidência disponível. Uma linha somente pode ser classificada como validada quando o teste ou a evidência existir. A matriz distingue documentação, implementação na `main` ou em branch de trabalho, validação em software, simulação e validação física.

## 9. Síntese aplicada ao projeto

A fundamentação sustenta a arquitetura de uma estação que combina sensores, ESP32, MicroPython, MQTT, backend Python, PostgreSQL, API REST e dashboard web. A literatura e as normas também sustentam a necessidade de rastreabilidade, qualidade de dados, acessibilidade, controle de dependências e distinção entre resultados projetados, simulados e fisicamente validados.

As fontes não permitem concluir que o protótipo possui determinada exatidão, disponibilidade, segurança, representatividade ou estabilidade. Essas conclusões exigirão testes próprios, calibração, documentação do sítio, comparação com referência quando aplicável e evidências reproduzíveis. Enquanto esses insumos não existirem, pinagem, calibração, conversão do pluviômetro, coordenadas e resultados físicos permanecem pendentes ou bloqueados.

## 10. Referências

[1]: https://www.mdpi.com/1424-8220/24/7/2074 "Sensors on Internet of Things Systems for the Sustainable Development of Smart Cities: A Systematic Literature Review"
[2]: https://www.mdpi.com/1424-8220/20/11/3113 "Advances in Smart Environment Monitoring Systems Using IoT and Sensors"
[3]: https://www.iso.org/standard/69050.html "ISO 37122:2019 — Sustainable cities and communities: Indicators for smart cities"
[4]: https://documentation.espressif.com/esp32_datasheet_en.html "ESP32 Series Datasheet, Version 5.3"
[5]: https://docs.micropython.org/en/latest/esp32/quickref.html "Quick reference for the ESP32 — MicroPython documentation"
[6]: https://www.mdpi.com/2079-9292/12/1/143 "Performance Evaluation of C/C++, MicroPython, Rust and TinyGo Programming Languages on ESP32 Microcontroller"
[7]: https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html "MQTT Version 5.0"
[8]: https://doi.org/10.1007/s40808-023-01701-w "Modeling and implementation of a low-cost IoT-smart weather monitoring station and air quality assessment based on fuzzy inference model and MQTT protocol"
[9]: https://community.wmo.int/site/knowledge-hub/programmes-and-initiatives/instruments-and-methods-of-observation-programme-imop/siting-classification "Siting Classification — WMO/ISO guidance for surface observing stations on land"
[10]: https://www.epa.gov/air-sensor-toolbox/how-use-air-sensors-air-sensor-guidebook "How to Use Air Sensors: Air Sensor Guidebook / Enhanced Air Sensor Guidebook"
[11]: https://journals.sagepub.com/doi/10.1177/0309133320956567 "Low-cost electronic sensors for environmental research: Pitfalls and opportunities"
[12]: https://www.mdpi.com/1424-8220/19/5/1185 "Boosting a Weather Monitoring System in Low Income Economies Using Open and Non-Conventional Systems: Data Quality Analysis"
[13]: https://www.rfc-editor.org/rfc/rfc9110 "RFC 9110 — HTTP Semantics"
[14]: https://peps.python.org/pep-0249/ "PEP 249 — Python Database API Specification v2.0"
[15]: https://www.postgresql.org/docs/current/ddl-constraints.html "PostgreSQL Documentation — Constraints"
[16]: https://www.sciencedirect.com/science/article/pii/S1364815225000210 "A real-time and modular weather station software architecture based on microservices"
[17]: https://www.mdpi.com/2077-0472/12/1/35 "An Agile AI and IoT-Augmented Smart Farming: A Cost-Effective Cognitive Weather Station"
[18]: https://www.w3.org/TR/WCAG22/ "Web Content Accessibility Guidelines (WCAG) 2.2"
[19]: https://www.w3.org/TR/geolocation/ "Geolocation"
[20]: https://www.iso.org/standard/63712.html "ISO/IEC/IEEE 12207:2017 — Systems and software engineering — Software life cycle processes"
[21]: https://standards.ieee.org/standard/29148-2018.html "IEEE/ISO/IEC 29148-2018 — Systems and software engineering — Life cycle processes — Requirements engineering"
[22]: https://www.iso.org/standard/81291.html "ISO/IEC/IEEE 29119-1:2022 — Software and systems engineering — Software testing — Part 1: General concepts"
[23]: https://www.sciencedirect.com/science/article/abs/pii/S0263224109001584 "Weather measurements traceability: An example at INRiM"
