# Guia de preparação da entrega N2

## Situação verificada em 04/11/2026

- Firmware Arduino DEV 1.1: DHT22, OLED, chuva digital e LDR digital implementados; comunicação por USB serial.
- Ponte `tools/serial_bridge.py`: interpreta leituras DHT22 e envia via POST HTTP ao backend local; chuva e luz são estados digitais no terminal, não valores quantitativos na API.
- Dashboard Clima iOS: consulta API REST; integração física ESP32 → dashboard ainda exige execução em bancada.
- Arquitetura alvo MQTT/PostgreSQL permanece separada do ensaio experimental USB/HTTP.

## Checklist de aceite (não marcar sem evidência)

- [ ] Confirmar pinos e alimentação dos módulos reais; soldar BMP/BME desconectado.
- [ ] Registrar firmware gravado e resultado de compilação.
- [ ] Executar testes de software no commit da entrega e anexar logs.
- [ ] Validar ESP32 por USB serial, ingestão HTTP e dashboard com timestamps reais.
- [ ] Validar Wi-Fi pessoal, Wi-Fi UNIP e provisionamento de rede de terceiro, conforme protocolo.
- [ ] Testar reconexão e recuperação após queda de rede.
- [ ] Atualizar matriz de rastreabilidade e relatório N2 com resultados reais.
- [ ] Receber instruções do vídeo, produzir roteiro e capturar demonstração.
- [ ] Revisar documentação e requisitos específicos das entregas de 13 e 16/11.

## Comandos para validação local no Windows

No PowerShell na raiz do repositório:

```powershell
python -m pip install -r backend/requirements.txt
python -m pip install pyserial
$env:PYTHONPATH="backend"
python -m pytest backend/tests frontend/tests -q
```

Para teste real pela USB, seguir `docs/integracao/ensaio-serial-dev-1.1.md`. Nunca publicar credenciais nem habilitar ingestão HTTP sem autenticação fora de `127.0.0.1`.

## Evidências

Para cada teste registrar: responsável, data, commit, hardware, condições, procedimento, resultado esperado, resultado observado, logs/fotos e aprovação. Testes não executados permanecem pendentes.
