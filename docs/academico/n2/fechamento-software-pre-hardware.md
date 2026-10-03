# Fechamento do software pré-hardware — N2

## Objetivo

Registrar o último gate de integração executável sem ESP32 e sensores físicos.

A etapa conecta componentes reais de software em vez de chamar diretamente as funções internas do backend.

## Fluxo validado no CI

```text
publisher Paho sintético
        ↓
broker Mosquitto real
        ↓
worker Paho MQTT
        ↓
PostgreSQL 16
        ↓
FastAPI
        ↓
API REST
        ↓
dashboard servido pelo backend
```

O teste é executado em ambiente de CI e utiliza telemetria sintética compatível com o contrato v1.0.

## O que o ensaio verifica

O teste:

1. inicia PostgreSQL;
2. aplica a migration oficial;
3. inicia um broker Mosquitto real;
4. inicia o worker MQTT em processo separado;
5. inicia o FastAPI em outro processo;
6. publica uma mensagem no tópico `estacao/<station_id>/telemetry`;
7. deixa o worker receber a mensagem por MQTT;
8. valida e persiste a telemetria no PostgreSQL;
9. consulta a mesma estação pela API REST;
10. verifica histórico;
11. verifica que o dashboard é servido pelo backend.

A mensagem de teste é marcada como sintética e não constitui evidência de sensor físico.

## Resultado técnico esperado

O gate é considerado aprovado quando o workflow do PR conclui com sucesso e a medição publicada pelo broker pode ser recuperada pela API REST depois de passar pelo worker e pelo PostgreSQL.

## Limite atingido sem hardware

Após este gate, não resta uma lacuna relevante de integração de software entre:

- broker MQTT;
- backend consumidor;
- persistência PostgreSQL;
- API REST;
- entrega do dashboard.

As próximas validações principais exigem ao menos um dos seguintes elementos externos:

- ESP32;
- sensores reais;
- OLED;
- rede Wi-Fi usada pelo protótipo;
- configuração final do broker;
- credenciais/TLS do ambiente final;
- montagem elétrica;
- calibração/caracterização;
- ensaios de bancada ou campo.

## O que esta evidência não prova

Este ensaio não prova:

- publicação MQTT pelo ESP32;
- reconexão Wi-Fi/MQTT no microcontrolador;
- aquisição de DHT22, BMP280, MQ-135, LDR ou chuva;
- funcionamento da OLED;
- sincronização NTP no hardware;
- precisão ou calibração;
- estabilidade física;
- operação de campo.

O estado correto desta entrega é **integração de software validada sem hardware**, e não estação física concluída.
