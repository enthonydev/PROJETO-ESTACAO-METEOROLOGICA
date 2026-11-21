# Publicação MQTT da bancada

O firmware agora oferece publicação MQTT 3.1.1 QoS 0 opcional, em tarefa asyncio separada do agendamento dos sensores, da OLED e do Serial. Sem mqtt_config.json habilitado, mantém o comportamento USB existente. Broker indisponível provoca reconexão com timeout, sem espera síncrona pela rede. O fluxo físico MicroPython/USB/API/dashboard já foi confirmado pela equipe em 14/11/2026; a publicação MQTT também foi recebida no Mosquitto e persistida no PostgreSQL em bancada em 14/11. O teste de queda de rede exigiu intervenção e não aprovou a recuperação integral.

Configuração local na raiz do ESP32 (não versionar credenciais):

```json
{"enabled":true,"host":"192.168.1.10","port":1884,"station_id":"estacao-esp32-real"}
```

Usar IPv4 do notebook na mesma rede. O tópico é estacao/estacao-esp32-real/telemetry. Apenas temperatura/umidade são quantitativas; pressão DEMO, chuva digital e luz digital não se tornam pressão medida, milímetros ou porcentagem. O timestamp usa RTC em UTC ajustado pelo notebook. Se o RTC perder a data após falta total de energia, a publicação pausa até novo ajuste. NTP autônomo ainda não está implementado.

O broker do ensaio é Mosquitto local, porta TCP 1884 em rede privada, sem TLS. Recebimento no mosquitto_sub comprova chegada ao broker; QoS 0 não confirma persistência. O worker PostgreSQL continua sendo uma etapa separada; o dashboard não deve declarar transporte MQTT enquanto receber pela ponte USB.

Verificação: 31 testes de firmware, incluindo publicação TCP, CONNACK, reconexão e progresso de outra tarefa quando o broker fica silencioso. São testes em computador e não aprovação física no ESP32.

Fontes: https://docs.micropython.org/en/v1.26.0/library/asyncio.html e https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html
