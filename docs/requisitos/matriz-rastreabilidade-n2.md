# Matriz de rastreabilidade da N2 — estado pré-hardware

## 1. Objetivo

Esta matriz complementa, sem substituir, a matriz histórica da N1. Ela registra o estado técnico alcançado após a implementação do dashboard, API REST, PostgreSQL e consumidor MQTT.

## 2. Estados utilizados

| Estado | Significado |
|---|---|
| Implementado | Existe código ou configuração versionada na `main`. |
| Validado em software | Existe teste automatizado ou execução reproduzível sem hardware. |
| Validado em runtime | O componente foi executado em ambiente real de software, como PostgreSQL no CI. |
| Parcial | Parte do requisito foi implementada, mas existe dependência externa ou física. |
| Pendente de hardware | Depende de ESP32, sensores, montagem ou medição física. |
| Pendente de infraestrutura | Depende de broker, credenciais, TLS ou ambiente final. |

## 3. Requisitos funcionais

| ID | Estado N2 pré-hardware | Evidência principal |
|---|---|---|
| RF-01 | Validado em software | contrato v1.0, schemas e testes backend/MQTT |
| RF-02 | Pendente de hardware | serviço abstrato existe; DHT22 real não validado |
| RF-03 | Pendente de hardware | arquitetura aprovada; BMP280 real não validado |
| RF-04 | Pendente de hardware | campo `air_quality_raw` preservado; MQ-135 real não validado |
| RF-05 | Pendente de hardware | `luminosity_pct` preservado; LDR real não validado |
| RF-06 | Pendente de hardware | chuva permanece experimental e sem `mm` inventado |
| RF-07 | Parcial | backend valida timestamp e estação; origem física depende de NTP/ESP32 |
| RF-08 | Parcial | qualidade preservada e validada no backend; validação física no firmware pendente |
| RF-09 | Parcial | consumidor MQTT implementado e testado logicamente; publicação do ESP32 e broker real pendentes |
| RF-10 | Pendente de hardware | reconexão real Wi-Fi/MQTT depende do ESP32 |
| RF-11 | Validado em software | Pydantic, contrato, MQTT e testes de rejeição |
| RF-12 | Validado em runtime | PostgreSQL 16 no CI com migration, gravação e consulta |
| RF-13 | Validado em software | health, stations, latest, measurements e summary |
| RF-14 | Validado em software | dashboard integrado à API REST |
| RF-15 | Validado em software | histórico 24h, 7d e 30d |
| RF-16 | Parcial | frontend/API suportam localização; coordenadas reais pendentes |
| RF-17 | Validado em software | loading, erro, offline e ausência de histórico |
| RF-18 | Parcial | renderer e task em software; OLED física pendente |
| RF-19 | Parcial | serviço temporal em software; exibição física pendente |
| RF-20 | Pendente de hardware | NTP no ESP32 não validado |
| RF-21 | Parcial | baseline de uma OLED preservada; operação física pendente |
| RF-22 | Parcial | isolamento de falhas testado parcialmente; comportamento físico pendente |
| RF-23 | Parcial | logs básicos backend/MQTT; observabilidade integrada ainda limitada |

## 4. Requisitos não funcionais

| ID | Estado N2 pré-hardware | Evidência principal |
|---|---|---|
| RNF-01 | Validado em software | camadas API/service/repository e firmware estruturado |
| RNF-02 | Parcial | tasks estruturadas; concorrência real no ESP32 pendente |
| RNF-03 | Parcial | falhas simuladas e estados degradados; hardware pendente |
| RNF-04 | Validado em software | FastAPI em execução e testes |
| RNF-05 | Validado em runtime | PostgreSQL 16 no CI |
| RNF-06 | Parcial | TIMESTAMPTZ e ISO-8601; origem física depende de NTP |
| RNF-07 | Implementado | índice `station_id + measured_at` na migration |
| RNF-08 | Validado em software | dashboard consome API; não acessa banco |
| RNF-09 | Validado em software | responsividade, foco e checks estáticos |
| RNF-10 | Validado em software | schema, parâmetros REST e mensagem MQTT validados |
| RNF-11 | Documentado/verificado | política de segurança e ausência de credenciais versionadas |
| RNF-12 | Parcial | logging básico disponível; observabilidade avançada pendente |
| RNF-13 | Validado em software | schema v1.0 versionado e testado |
| RNF-14 | Parcial | várias camadas cobertas; broker real e hardware ainda ausentes |
| RNF-15 | Aplicado | simulação explicitamente separada de validação física |
| RNF-16 | Aplicado | evolução por branch, PR e checks |
| RNF-17 | Aplicado no fluxo | commits em português conforme governança vigente |
| RNF-18 | Aplicado | baseline e decisões estruturais mantidas em ADRs |
| RNF-19 | Em execução | N1 preservada e rastreabilidade N2 criada nesta etapa |
| RNF-20 | Validado em software | dashboard/API/banco reproduzíveis sem hardware |

## 5. Próximo gate sem hardware

O próximo gate técnico possível sem ESP32 é:

```text
publisher sintético
→ broker MQTT real
→ worker Paho
→ PostgreSQL
→ FastAPI
→ consulta REST/dashboard
```

Após esse gate, as principais pendências passam a ser físicas ou de infraestrutura final.
