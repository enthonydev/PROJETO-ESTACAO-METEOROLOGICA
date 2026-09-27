# Plano de testes de hardware e integração

**Classificação:** PLANEJADO / PENDENTE DE HARDWARE  
**Resultado observado:** NÃO EXECUTADO, salvo quando explicitamente classificado como teste de software.  
**Referência:** ADR-002.

Este plano substitui os testes da arquitetura com TCA9548A, duas OLEDs, BME280 adicional e DS3231.

| ID | Subsistema | Objetivo | Resultado esperado | Estado |
|---|---|---|---|---|
| HW-T01 | ESP32 | Confirmar boot e firmware | Boot estável e log identificável | PENDENTE |
| HW-T02 | Alimentação | Validar tensões/níveis | Dentro dos limites dos módulos reais | PENDENTE |
| HW-T03 | I²C | Identificar BMP280 e OLED | Endereços reais detectados e documentados | PENDENTE |
| HW-T04 | OLED única | Renderizar interface local | Conteúdo legível sem afetar aquisição | PENDENTE |
| HW-T05 | DHT22 | Ler temperatura/umidade | Leituras e falhas coerentes | PENDENTE |
| HW-T06 | BMP280 | Ler pressão | Unidade/conversão coerente | PENDENTE |
| HW-T07 | MQ-135 | Caracterizar leitura bruta | Raw documentado; sem ppm indevido | PENDENTE |
| HW-T08 | LDR | Caracterizar leitura relativa | Conversão relativa reproduzível | PENDENTE |
| HW-T09 | Sensor de chuva | Caracterizar resposta experimental | Detecção/resposta documentada; sem mm indevido | PENDENTE |
| HW-T10 | NTP | Sincronizar relógio | Sincronização registrada quando online | PENDENTE |
| HW-T11 | Operação sem internet | Verificar degradação | Sensores locais continuam; rede/tempo sinalizam limitação | PENDENTE |
| HW-T12 | API externa | Verificar falha/retorno | Falha não invalida sensores locais | PENDENTE |
| HW-T13 | Wi-Fi/MQTT | Perda e recuperação | Aquisição não congela; recuperação registrada | PENDENTE |
| HW-T14 | Falha de sensor | Isolar falha | Métrica afetada sinalizada; demais continuam | PENDENTE |
| HW-T15 | Recuperação de sensor | Restaurar componente | Retorno sem estado falso | PENDENTE |
| HW-T16 | Telemetria | Conferir mapeamento | Payload sem valores inventados | PENDENTE |
| HW-T17 | Integração geral | Sensor até backend | Caminho completo coerente | PENDENTE |
| HW-T18 | Estabilidade | Executar período definido | Reinícios/erros dentro do critério aprovado | PENDENTE |
| HW-T19 | Campo | Comparar comportamento ambiental | Série e limitações registradas | PENDENTE |

## Evidência obrigatória

Registrar ID, versão do código, data/hora, ambiente, modelo dos componentes, procedimento, esperado, observado, responsável e arquivo de evidência. Classificar como **FÍSICA** ou **SIMULADA**.

Testes automatizados com doubles comprovam apenas comportamento de software. Não aprovam HW-T01–HW-T19.
