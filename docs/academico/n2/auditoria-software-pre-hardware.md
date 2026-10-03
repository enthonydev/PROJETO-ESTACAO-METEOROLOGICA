# Auditoria técnica da N2 — estado pré-hardware

## 1. Escopo

Esta auditoria revisa a `main` após o merge do PR #29 e verifica quanto do projeto pode ser considerado implementado ou validado sem hardware físico.

A análise cobre contrato de telemetria, backend FastAPI, API REST, dashboard, PostgreSQL, processamento MQTT, testes automatizados e CI, coerência com requisitos e arquitetura, segurança básica dos caminhos auxiliares de desenvolvimento e limites que ainda dependem de infraestrutura ou hardware.

A auditoria não transforma simulação em evidência física.

## 2. Baseline auditada

Commit de `main` auditado no início desta revisão:

```text
5699811feabeac2a2cf91bea2cd8875b2f2720f5
```

O PR #29 foi mergeado e o workflow **Checks de documentação, contrato e código**, execução #69, terminou com sucesso.

## 3. Resultado geral

O núcleo de software previsto para consulta e visualização está substancialmente implementado antes da chegada do hardware.

Fluxos já disponíveis ou validados:

```text
dados sintéticos
    ↓
repository
    ↓
service
    ↓
FastAPI REST
    ↓
dashboard
```

```text
payload MQTT simulado
    ↓
validação de tópico + contrato
    ↓
repository
    ↓
API REST
```

```text
payload de teste
    ↓
PostgreSQL 16 no CI
    ↓
latest / history / summary
```

O fluxo físico completo ainda não está validado:

```text
sensores reais
    ↓
ESP32
    ↓
Wi-Fi
    ↓
broker MQTT real
    ↓
worker MQTT
    ↓
PostgreSQL
    ↓
API REST
    ↓
dashboard
```

## 4. Itens auditados

### 4.1 Contrato de telemetria

**Estado: validado em software.**

O schema v1.0 permanece como fonte normativa. Backend, exemplos e testes preservam `schema_version`, `station_id`, `timestamp`, `location`, `measurements` e `quality`.

O processamento MQTT também verifica que o `station_id` presente no tópico corresponde ao payload.

Não foi identificada necessidade de mudança de contrato nesta etapa.

### 4.2 API REST

**Estado: implementada e validada em software.**

Estão disponíveis:

```text
GET /health
GET /api/v1/stations
GET /api/v1/stations/{id}/latest
GET /api/v1/stations/{id}/measurements
GET /api/v1/stations/{id}/summary
POST /api/v1/telemetry/validate
```

O endpoint `POST /api/v1/telemetry` existe apenas como apoio de desenvolvimento.

Durante a auditoria foi identificado que esse caminho auxiliar ficava disponível por padrão. Isso poderia permitir escrita não planejada caso o backend fosse publicado dessa forma. A correção desta auditoria altera o comportamento para **desabilitado por padrão**, exigindo:

```text
ENABLE_HTTP_INGESTION=true
```

para uso explícito em desenvolvimento.

### 4.3 Dashboard

**Estado: implementado e integrado à API REST.**

A interface possui leitura atual, histórico multi-métrica, períodos de 24h/7d/30d, mínimo/média/máximo, estados de qualidade, loading, erro, offline, ausência de histórico, exportação CSV, responsividade, acessibilidade básica e cenários controlados de demonstração.

Quando servido pelo FastAPI, o frontend consome a API na mesma origem. Quando aberto diretamente como arquivo, entra no modo de demonstração.

Não há acesso direto do frontend ao PostgreSQL.

### 4.4 PostgreSQL

**Estado: implementado e validado em runtime no CI.**

A migration cria `stations`, `measurements`, `measurement_quality` e índice composto de estação e instante.

O repositório PostgreSQL implementa gravação e consultas de última leitura, histórico e resumo.

O CI inicia PostgreSQL 16, aplica a migration, grava telemetria e verifica leitura de volta. Portanto, neste ponto não é correto registrar PostgreSQL apenas como “projetado”.

A validação é de software/runtime em ambiente de CI, não evidência física.

### 4.5 MQTT

**Estado: processamento implementado; transporte real ainda não validado.**

O backend possui parser de tópico, validação JSON, validação do contrato, correspondência tópico/payload, persistência via interface de repositório e worker Paho MQTT.

Testes exercitam mensagens MQTT simuladas e o caminho até a API REST.

Durante a auditoria foi identificado um problema de processo: o worker MQTT é executado separadamente do FastAPI. Se ambos usassem `InMemoryMeasurementRepository`, cada processo teria sua própria memória e uma mensagem recebida pelo worker não apareceria na API.

A correção desta auditoria faz o worker separado exigir `DATABASE_URL`. Assim, worker e API compartilham PostgreSQL e não há falsa impressão de integração usando memórias independentes.

### 4.6 CI e testes

**Estado: consistente para a etapa atual.**

O workflow cobre arquivos essenciais, JSON/schema, contrato, backend, firmware estrutural, frontend estático, compilação Python e PostgreSQL em runtime.

O PR #29 chegou à `main` com CI concluído com sucesso.

Esta auditoria acrescenta cobertura para ingestão HTTP desabilitada por padrão, execução controlada da ingestão HTTP em teste e bloqueio do worker MQTT quando não existe armazenamento compartilhado.

## 5. Coerência com os requisitos

### Requisitos já substancialmente atendidos em software

RF-01, RF-11, RF-12, RF-13, RF-14, RF-15 e RF-17 possuem implementação e evidência de software compatível com a etapa atual.

RNF-01, RNF-04, RNF-05, RNF-07, RNF-08, RNF-09, RNF-10, RNF-13, RNF-14, RNF-15, RNF-16 e RNF-20 também possuem evidência técnica ou documental suficiente para o estágio pré-hardware.

### Requisitos parcialmente atendidos

- RF-09: lado consumidor MQTT implementado, mas publicação real do firmware e broker real não validados;
- RF-10: estratégia de reconexão do firmware ainda depende de execução no ESP32;
- RF-16: suporte existe, mas coordenadas reais ainda não foram aprovadas;
- RF-22: comportamento degradado possui cobertura parcial em software;
- RF-23 / RNF-12: há logs no worker/backend, mas observabilidade integrada ainda pode evoluir;
- RNF-06: UTC está preservado em banco/contrato, mas o caminho físico de origem do timestamp depende do ESP32/NTP;
- RNF-19: a matriz da N1 está correta como documento histórico, porém ficou naturalmente desatualizada para o estado da N2.

### Requisitos dependentes de hardware

RF-02 a RF-08 no aspecto físico, RF-10 na recuperação real, RF-18 a RF-21 e partes de RF-22 dependem dos módulos reais, montagem, pinagem e testes.

## 6. Achados da auditoria

### A-01 — endpoint HTTP de ingestão aberto por padrão

**Severidade:** média.  
**Situação:** corrigido nesta auditoria.

O endpoint auxiliar de escrita existia para desenvolvimento, mas ficava exposto sempre que o backend fosse executado. Agora exige ativação explícita por variável de ambiente.

### A-02 — repositório em memória não é compartilhado entre worker e API

**Severidade:** alta para integração MQTT.  
**Situação:** corrigido nesta auditoria.

O teste em processo único era válido como teste lógico, mas não representava dois processos reais. O worker separado agora exige PostgreSQL configurado.

### A-03 — matriz de rastreabilidade da N1 não representa o estado atual

**Severidade:** documental.  
**Situação:** preservar a matriz da N1.

A matriz N1 deve permanecer como registro histórico daquela entrega. A solução correta é manter o avanço da N2 em documentos próprios em vez de reescrever o passado.

### A-04 — broker MQTT real ainda não participa do CI

**Severidade:** pendência de integração, não bloqueador de hardware.

Os testes validam o processamento da mensagem, mas não exercitam conexão TCP real com um broker, subscribe, publish e callback Paho em um ciclo completo.

Esse é o principal item restante que ainda pode ser realizado **sem ESP32**.

### A-05 — autenticação/TLS do broker ainda não foi definida

**Severidade:** pendência de infraestrutura.

A infraestrutura final do broker está registrada como TBD nos requisitos. Usuário, senha, TLS e política de acesso só devem ser implementados quando o ambiente de broker for definido, sem versionar segredos.

### A-06 — observabilidade ainda é básica

**Severidade:** baixa nesta etapa.

Há logs de conexão e mensagens aceitas/rejeitadas no worker, mas ainda não existe correlação, métricas ou persistência de eventos operacionais. Não é necessário para fechar o protótipo acadêmico atual, mas permanece evolução possível.

## 7. O que ainda pode ser feito sem hardware

Há um bloco técnico claro antes de depender fisicamente do ESP32:

1. executar um broker MQTT real em ambiente de CI ou desenvolvimento;
2. publicar telemetria de teste no broker;
3. executar o worker MQTT conectado a esse broker;
4. persistir a mensagem no PostgreSQL;
5. consultar a mesma medição pela API REST;
6. verificar o resultado que o dashboard consumiria.

Esse ensaio produzirá evidência de integração de software:

```text
publisher sintético
    ↓
broker MQTT real
    ↓
worker Paho MQTT
    ↓
PostgreSQL
    ↓
FastAPI
    ↓
consulta REST
```

Depois disso, o bloqueio principal passa de software para hardware/infraestrutura final.

## 8. Itens que devem esperar hardware

- drivers físicos definitivos;
- pinagem definitiva;
- níveis elétricos;
- endereços I²C;
- DHT22 real;
- BMP280 real;
- MQ-135 real e caracterização;
- LDR real e conversão relativa;
- módulo de chuva;
- OLED física;
- NTP no ESP32;
- Wi-Fi e reconexão no microcontrolador;
- publicação pelo ESP32;
- estabilidade em bancada;
- calibração/caracterização;
- testes de campo;
- evidências físicas HW-T01 a HW-T19.

## 9. Conclusão

A auditoria não identificou incompatibilidade estrutural entre o contrato v1.0, API REST, dashboard, modelo PostgreSQL e processamento MQTT.

Foram encontrados dois riscos concretos de integração, ambos corrigidos na própria auditoria: exposição padrão da ingestão HTTP auxiliar e uso indevido de memória isolada no worker MQTT separado.

Com essas correções, a principal frente ainda executável sem hardware é a validação com **broker MQTT real + PostgreSQL + worker + API REST**. Depois desse ensaio, a maior parte das pendências restantes exigirá ESP32, sensores ou decisões de infraestrutura final.
