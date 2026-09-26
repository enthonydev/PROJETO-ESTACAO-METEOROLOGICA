# Plano de testes de hardware e integração

**Classificação atual:** PLANEJADO / PENDENTE DE HARDWARE  
**Resultado observado de todos os testes abaixo:** `NÃO EXECUTADO`  
**Evidência física disponível:** nenhuma.

Este plano prepara a bancada sem transformar planejamento, simulação, fixture ou teste automatizado em validação física.

| ID | Componente/subsistema | Objetivo | Pré-condições | Procedimento resumido | Resultado esperado | Resultado observado | Evidência | Estado |
|---|---|---|---|---|---|---|---|---|
| HW-T01 | ESP32 | Confirmar boot e execução do firmware | ESP32 real, firmware preparado, alimentação segura | Energizar, registrar versão, saída serial e reinicializações | Boot estável e log identificável | NÃO EXECUTADO | Log/foto a registrar | PENDENTE DE HARDWARE |
| HW-T02 | ESP32/serial | Confirmar saída serial de diagnóstico | HW-T01 concluído | Capturar inicialização, falhas e recuperação | Log sem segredos e com eventos relevantes | NÃO EXECUTADO | Arquivo de log | PENDENTE DE HARDWARE |
| HW-T03 | Alimentação | Verificar alimentação e níveis do circuito | Modelos/datasheets e instrumento apropriado | Conferir tensão sob operação e condições de carga | Dentro dos limites dos componentes | NÃO EXECUTADO | Medições/fotos | PENDENTE DE HARDWARE |
| HW-T04 | Barramento I²C | Identificar dispositivos e endereços reais | Montagem segura e módulos reais | Executar scan I²C por configuração de barramento | Endereços observados correspondem aos módulos | NÃO EXECUTADO | Log do scan | PENDENTE DE HARDWARE |
| HW-T05 | TCA9548A | Confirmar seleção do multiplexador | HW-T04 e endereço do TCA confirmado | Selecionar canais e observar resposta | Canal selecionado responde sem interferir indevidamente | NÃO EXECUTADO | Log/serial | PENDENTE DE HARDWARE |
| HW-T06 | OLED CH0 | Testar OLED meteorológico no canal 0 | HW-T05 e display real | Selecionar CH0 e renderizar estado meteorológico | OLED #1 exibe conteúdo correto | NÃO EXECUTADO | Foto/log | PENDENTE DE HARDWARE |
| HW-T07 | OLED CH1 | Testar OLED relógio no canal 1 | HW-T05 e display real | Selecionar CH1 e renderizar relógio/calendário | OLED #2 exibe conteúdo correto | NÃO EXECUTADO | Foto/log | PENDENTE DE HARDWARE |
| HW-T08 | Dois OLEDs | Confirmar atualização independente | HW-T06/HW-T07 | Atualizar conteúdos diferentes e alternar canais | Uma tela não corrompe a outra | NÃO EXECUTADO | Vídeo/log/fotos | PENDENTE DE HARDWARE |
| HW-T09 | BME280 | Confirmar leitura local | Modelo/datasheet e driver aprovado | Ler temperatura, umidade e pressão; registrar unidade e estabilidade | Leituras recebidas e limites documentados | NÃO EXECUTADO | Log/série de dados | PENDENTE DE HARDWARE |
| HW-T10 | DS3231 | Confirmar relógio local | RTC real e procedimento de ajuste | Ajustar/ler RTC, desligar rede e verificar continuidade | Hora local permanece disponível dentro do critério aprovado | NÃO EXECUTADO | Log/fotos | PENDENTE DE HARDWARE |
| HW-T11 | NTP/RTC | Confirmar correção controlada | Rede e RTC reais | Sincronizar NTP, comparar, registrar correção e falha | Correção documentada sem quebrar o fallback local | NÃO EXECUTADO | Log | PENDENTE DE HARDWARE |
| HW-T12 | Operação sem internet | Confirmar comportamento degradado | Montagem funcional | Remover conectividade e observar displays, aquisição e RTC | Funções locais continuam quando possível; falha é registrada | NÃO EXECUTADO | Log/vídeo | PENDENTE DE HARDWARE |
| HW-T13 | Wi-Fi/MQTT | Confirmar perda e recuperação | Broker e rede autorizados | Interromper/restaurar rede e observar tentativas controladas | Aquisição não congela; recuperação registrada | NÃO EXECUTADO | Log do dispositivo/broker | PENDENTE DE HARDWARE |
| HW-T14 | DHT22/BMP280 | Testar sensores adicionais se decisão dos POs mantiver ambos | Componentes reais e decisão de escopo | Ler individualmente e comparar com o mapeamento aprovado | Grandezas e unidades coerentes | NÃO EXECUTADO | Log | PENDENTE DE HARDWARE / DECISÃO |
| HW-T15 | MQ-135 | Caracterizar indicador bruto | Circuito, método e referência aprovados | Registrar leitura bruta e condições; não declarar ppm sem calibração | Raw e qualidade documentados | NÃO EXECUTADO | Série/log | PENDENTE DE HARDWARE/CALIBRAÇÃO |
| HW-T16 | LDR | Definir leitura relativa | Divisor e unidade aprovados | Medir condições controladas e documentar conversão | Unidade/conversão reproduzível | NÃO EXECUTADO | Série/log | PENDENTE DE HARDWARE |
| HW-T17 | Pluviômetro | Definir pulsos e conversão | Modelo real e fator aprovado | Registrar pulsos e comparar com volume de referência | `rain_mm` sustentado por conversão documentada | NÃO EXECUTADO | Série/planilha | PENDENTE DE HARDWARE/CALIBRAÇÃO |
| HW-T18 | Falha de sensor | Verificar isolamento de falha | Montagem e procedimento seguro | Simular/desconectar conforme permitido e observar demais métricas | Métrica afetada sinalizada; demais funções continuam quando possível | NÃO EXECUTADO | Log | PENDENTE DE HARDWARE |
| HW-T19 | Recuperação | Verificar retorno de componente | HW-T18 e procedimento aprovado | Restaurar componente e observar recuperação | Retorno registrado e sem estado falso | NÃO EXECUTADO | Log | PENDENTE DE HARDWARE |
| HW-T20 | Integração geral | Verificar caminho local até telemetria | Hardware, firmware, Wi-Fi, broker e contrato prontos | Executar aquisição, qualidade, serialização e publicação | Payload coerente no tópico esperado | NÃO EXECUTADO | Payload/log | PENDENTE DE HARDWARE/INTEGRAÇÃO |
| HW-T21 | Estabilidade | Observar ciclos e falhas ao longo do período aprovado | Montagem e critério temporal definidos | Executar por período definido e registrar reinícios/erros | Critério de estabilidade aprovado atendido | NÃO EXECUTADO | Log/série | PENDENTE DE HARDWARE |
| HW-T22 | Telemetria resultante | Conferir mapeamento dos campos do contrato | HW-T20 e contrato v1.0 | Comparar grandeza, unidade, qualidade e timestamp | Campos sem valor inventado e com estados coerentes | NÃO EXECUTADO | Payload e relatório | PENDENTE DE HARDWARE |

## Regras de evidência

Cada execução futura deve registrar: ID do teste, versão do código, data/hora, ambiente, componentes/modelos, procedimento, resultado esperado, resultado observado, responsável, arquivo de evidência e classificação **FÍSICA** ou **SIMULADA**. Fotos, logs, vídeos e séries somente devem ser vinculados depois de realmente produzidos.

Os testes automatizados atuais do firmware e os fixtures do backend comprovam comportamento de software/simulação. Eles não substituem os testes HW-T01–HW-T22.
