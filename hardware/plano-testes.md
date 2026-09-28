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

## Procedimento quando as peças chegarem

Esta sequência deve ser executada e registrada antes de marcar qualquer HW-Txx como aprovado. Os componentes reais ainda não estão disponíveis; portanto, todos os itens abaixo são preparação operacional.

1. Registrar o anúncio, pedido ou comprovante de compra e a data de recebimento.
2. Fotografar as embalagens e registrar fabricante, modelo, revisão, marcações da placa e quantidade efetivamente recebida. Quando não for possível identificar algum dado, registrar `TBD`.
3. Localizar a documentação do fabricante correspondente ao modelo recebido. Não usar o datasheet de um módulo semelhante como se fosse o módulo real.
4. Conferir no datasheet a alimentação, os níveis lógicos, a interface, os limites elétricos e as condições de operação de cada módulo.
5. Somente depois dessa conferência, propor GPIOs e registrar a análise de ADC1, boot/strapping, Wi-Fi, conflitos e pull-ups no `hardware/pinout.md`. Nenhum GPIO definitivo deve ser escolhido por antecipação.
6. Inspecionar protoboard, jumpers, conectores, polaridade e isolamento; revisar o mapa de interconexões antes de energizar.
7. Testar o ESP32 isoladamente: alimentação compatível, boot, versão do firmware e saída serial, registrando HW-T01 e HW-T02.
8. Testar a alimentação e os níveis do circuito sem conectar todos os periféricos, complementando as evidências de HW-T02 com as medições correspondentes.
9. Testar cada sensor individualmente: DHT22, BMP280, MQ-135, LDR e módulo de chuva, usando os IDs HW-T05 a HW-T09. MQ-135 deve permanecer raw/experimental; LDR deve permanecer relativo; chuva não deve gerar `rain_mm` quantitativo sem método/fator validado.
10. Verificar o barramento I²C e registrar os endereços efetivamente encontrados do BMP280 e da OLED em HW-T03. O endereço continua dependente do módulo real.
11. Testar a única OLED isoladamente em HW-T04, confirmando legibilidade e que falha da interface não impede a aquisição.
12. Integrar os sensores progressivamente, um por vez, repetindo os testes de aquisição e observando conflitos elétricos, de GPIO ou de software.
13. Testar NTP em condição conectada com HW-T10, registrando fonte temporal, timestamp e falhas. Não há DS3231 na baseline.
14. Testar a condição sem internet com HW-T11. Registrar que a ausência de RTC dedicado limita a manutenção temporal offline; não ocultar nem inventar timestamp confiável.
15. Testar API externa complementar, Wi-Fi/MQTT, perda e recuperação, falha e recuperação de sensor, telemetria, integração geral e estabilidade com HW-T12 a HW-T18.
16. Executar o teste de campo HW-T19 somente quando houver montagem física apta e condições definidas para a comparação ambiental; até lá, mantê-lo `PENDENTE`.
17. Registrar cada execução com ID, data/hora, commit, componente/modelo, ambiente, procedimento, esperado, observado, responsável, arquivo/log/foto e classificação `FÍSICA` ou `SIMULADA`. Somente então avaliar o resultado contra o critério de aceite; planejamento ou fixture não é aprovação.
