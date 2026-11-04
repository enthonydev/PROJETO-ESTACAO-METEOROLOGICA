# Ensaio N2 — ESP32 Wi-Fi, broker MQTT, PostgreSQL e Dashboard

**Preparado, não validado fisicamente.** O firmware DEV 1.1 de bancada fica preservado. Versão N2 exige revisão da montagem e validação de sensores opcionais.

## 1. Rede e ESP32

- ESP32 tradicional trabalha em Wi-Fi **2,4 GHz**; rede apenas 5 GHz não é compatível.
- `WiFi.begin(ssid, senha)` atende Wi-Fi pessoal (ex.: WPA2-Personal), mas **não** se conecta automaticamente a portal cativo ou WPA2-Enterprise/802.1X de instituição.
- A UNIP pode usar rede de convidados ou infraestrutura com restrições. Verifique nome/tipo de segurança com a equipe de TI; não tente contornar autenticação nem isolamento de clientes.
- Só use a rede de outra pessoa com **autorização explícita** e as credenciais fornecidas por ela.
- O ESP32 só alcança o broker se tiver rota IP e se firewall/roteador permitirem TCP 1883.
- Para reduzir risco de exposição, preferir hotspot privado do notebook/celular durante o teste de integração MQTT e documentar separadamente o teste de associação à UNIP.

### Preparar firmware

1. Abrir `firmware/arduino/Estacao_Integrada_N2/Estacao_Integrada_N2.ino` no Arduino IDE.
2. Criar na mesma pasta `local_config.h` copiando `local_config.example.h`, e preencher apenas no computador local: três SSIDs/senhas e o IP **LAN** do computador que hospeda o broker.
3. Instalar bibliotecas **PubSubClient**, **Adafruit SSD1306**, **Adafruit GFX**, **DHT sensor library** e dependências. Instalar **Adafruit BMP280 Library** OU **Adafruit BME280 Library** somente se a opção correspondente estiver habilitada, após identificar fisicamente o sensor.
4. Na primeira execução deixar `ENABLE_BMP280=0`, `ENABLE_BME280=0`, `ENABLE_MQ135=0`, `ENABLE_LDR_ANALOG=0`. Assim não mudamos o hardware validado.
5. Após instalar e compilar, enviar a nova versão **somente quando a equipe aprovar**. A baseline DEV 1.1 permanece disponível para rollback.
6. Monitor Serial 115200: comandos `wifi 1`, `wifi 2`, `wifi 3`, `status`. Redefinir conexão cancela tentativa anterior. Não exibir senha em vídeos/logs.
7. Com Wi-Fi conectado, aguardar NTP; sem timestamp UTC válido o firmware **não** publica mensagem como se fosse recente.

### Teste de estresse de redes

| Caso | Rede | Evidência mínima |
| --- | --- | --- |
| NET-T01 | Wi-Fi residencial autorizado | associação, IP local, horário NTP, estabilidade e reconexão |
| NET-T02 | Wi-Fi UNIP autorizado | segurança da rede, conexão, IP, obstáculos (captive portal/802.1X/client isolation) |
| NET-T03 | Outra rede de pessoa autorizada | associação, perda/retorno, transição e reconexão |

Critérios de aceite **a confirmar com o professor**, pois ele não forneceu duração, número de reconexões nem taxa máxima de falhas ainda. Sugestão de coleta: log inicial, 10 min por rede e 3 ciclos de desconexão/reconexão, caso autorizado. Não classificar como aprovado sem coleta real.

## 2. Banco e broker local (opcional: Docker Desktop)

O **teste inicial de dashboard via USB serial não precisa de Docker nem PostgreSQL**. Para a arquitetura MQTT real, o worker roda separado e precisa de PostgreSQL compartilhado.

Em PowerShell, na raiz do projeto, com Docker Desktop instalado:

```powershell
Copy-Item deploy/local/env.example .env
# Edite .env e altere POSTGRES_PASSWORD para senha local forte, nao publique.
docker compose -f deploy/local/docker-compose.yml --env-file .env up -d postgres
```

Criar senha do broker (executar depois de confirmar Docker; senha pedida interativamente):

```powershell
docker compose -f deploy/local/docker-compose.yml --env-file .env run --rm --entrypoint mosquitto_passwd broker -c /mosquitto/secrets/passwords estacao
docker compose -f deploy/local/docker-compose.yml --env-file .env up -d broker
```

O broker escuta na porta 1883 para clientes autorizados na LAN. Não exponha essa porta à Internet. Verifique as regras de firewall do Windows. A senha MQTT precisa estar no `local_config.h` (não versionado).

Criar tabelas, no mesmo PowerShell:

```powershell
Get-Content database/migrations/001_schema_inicial.sql | docker compose -f deploy/local/docker-compose.yml --env-file .env exec -T postgres psql -U estacao -d estacao
```

Definir `DATABASE_URL` no ambiente local e iniciar backend + worker em **terminais separados**. Substitua o exemplo por suas credenciais locais, sem copiá-las para chat, GitHub ou vídeo:

Terminal 1:
```powershell
$env:PYTHONPATH="backend"
$env:DATABASE_URL="postgresql://estacao:SENHA_LOCAL@127.0.0.1:5432/estacao"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Terminal 2:
```powershell
$env:PYTHONPATH="backend"
$env:DATABASE_URL="postgresql://estacao:SENHA_LOCAL@127.0.0.1:5432/estacao"
$env:MQTT_BROKER_HOST="127.0.0.1"
$env:MQTT_USERNAME="estacao"
$env:MQTT_PASSWORD="SENHA_BROKER_LOCAL"
python -m app.workers.mqtt_consumer
```

**Observações**:
- Evite senhas contendo caracteres especiais não codificados no URL PostgreSQL; encode corretamente ou configure por um mecanismo seguro de ambiente.
- Se o Docker Desktop ou o broker não funcionar, não inventar sucesso: coletar erro e ajustar.
- Não habilitar `ENABLE_HTTP_INGESTION=true` para esse cenário MQTT, a menos que a equipe teste o caminho USB separadamente.
- `tools/serial_bridge.py` usa o Monitor Serial e HTTP para facilitar depuração; NÃO é a prova de MQTT Wi-Fi.

## 3. Teste do dashboard com valores reais

```powershell
python scripts/check_live_station.py --station estacao-esp32-real
```

`[OK]` comprova que a API retornou temperatura/umidade recentes com qualidade válida. **Sozinha, essa verificação não prova a origem MQTT**: guardar junto o log do ESP32 publicando, o log do consumidor e consulta PostgreSQL.

Painel:
```text
http://127.0.0.1:8000/dashboard/?station=estacao-esp32-real
```

Sensores opcionais só devem aparecer como reais se a leitura respectiva estiver validada e integrada. Chuva DO não mede mm; LDR DO não mede porcentagem. O tópico `estacao/<station_id>/digital` é diagnóstico auxiliar, não parte do contrato MQTT de medidas numéricas v1.0; o dashboard ainda não exibe esses dois estados remotos.

## 4. Registro

Para cada teste, guardar: ID, data/hora, rede (nome pode ser anonimizado), tipo de autenticação, firmware/commit, expectativa, resultado real, log sem senhas, fotos do hardware e tela final. `docs/academico/n2/plano-fechamento-13-16-novembro.md` mantém o checklist geral.
