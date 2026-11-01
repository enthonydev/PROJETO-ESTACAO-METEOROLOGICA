# Integração experimental pela USB serial (Arduino DEV 1.1)

## Finalidade

Validar a cadeia de dados reais **ESP32 → USB serial → ponte Python → POST HTTP local → FastAPI → dashboard**, sem alterar o firmware validado. Este caminho é provisório; não substitui o MQTT previsto pela arquitetura.

**Limite do contrato:** temperatura e umidade são medidas numéricas reais. O serial fornece **apenas estados digitais** de chuva e luz. A ponte os exibe em seu terminal, mas não inventa `rain_mm` nem `luminosity_pct`. Por isso o dashboard atual mostra **Sem dado** para chuva quantitativa e luminosidade percentual até existir extensão explícita de contrato/interface.

## Pré-requisitos

- Windows, ESP32 com firmware `firmware/arduino/Estacao_Meteorologica_DEV_1_1/Estacao_Meteorologica_DEV_1_1.ino` já gravado.
- Python 3.10+.
- Porta USB serial do ESP32 conhecida (no teste foi COM7; confirme no Gerenciador de Dispositivos).
- Arduino IDE **Monitor Serial fechado** para liberar a porta para a ponte.
- Nenhum banco de dados obrigatório para este ensaio: o backend mantém os dados novos em memória enquanto o processo roda. **Reiniciar o backend apaga esses dados reais em memória**. PostgreSQL deve ser configurado para histórico persistente.

## Instalação

Abra o PowerShell **na raiz do repositório**:

```powershell
python -m pip install -r backend/requirements.txt
python -m pip install pyserial
```

## Terminal 1 — iniciar backend local

```powershell
$env:PYTHONPATH="backend"
$env:ENABLE_HTTP_INGESTION="true"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Não use `--workers` múltiplos para essa sessão em memória.

Teste no navegador: `http://127.0.0.1:8000/health`.

## Terminal 2 — ponte com o ESP32

Com o Monitor Serial fechado e o ESP32 ligado pela USB:

```powershell
python tools/serial_bridge.py --port COM7
```

O script deve mostrar `Enviado: XX.X C; YY.Y% UR` a cada nova leitura DHT22. Ele também imprime estados digitais de chuva e luz quando os logs do firmware os informam. Se sua porta não for COM7, substitua.

## Dashboard real

Abra:

```text
http://127.0.0.1:8000/dashboard/?station=estacao-esp32-real
```

A estação `estacao-01` é a estação **sintética** antiga. A `estacao-esp32-real` é isolada para as novas leituras do ESP32. O dashboard atualiza automaticamente a cada 60 s ou pelo botão manual.

Se aparecer HTTP 404, confirme que a ponte recebeu e enviou uma leitura DHT22 **depois** que o backend iniciou.

## Limites e segurança

- O endpoint HTTP para ingestão é habilitado **apenas** com `ENABLE_HTTP_INGESTION=true`. Mantenha o servidor em `127.0.0.1` nesta fase; não exponha essa ingestão sem autenticação na rede.
- Este ensaio não prova Wi-Fi, MQTT, NTP, reinicialização do ESP32 nem estabilidade prolongada.
- O relógio usado nos timestamps da ponte vem do **computador**, não do ESP32 (a origem temporal deve ser registrada como tal).
- `rain_mm`, `luminosity_pct`, `pressure_hpa` e `air_quality_raw` permanecem `null` até medições compatíveis.
- Os indicadores digitais de chuva/luz continuam validados na OLED e no terminal, mas ainda não aparecem como estados dedicados no dashboard do contrato v1.0.
- Não conecte o MQ-135 sem revisão de alimentação e condicionamento de saída; o módulo é 5 V.
