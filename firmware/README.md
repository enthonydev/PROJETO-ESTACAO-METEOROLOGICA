# Firmware

Firmware MicroPython do ESP32. A pinagem deve seguir a documentação validada em `hardware/`.

## Wi-Fi no MicroPython

Copie os arquivos de `firmware/src/` para a raiz do sistema de arquivos do
ESP32 com MicroPython. Pela USB, usando Thonny ou mpremote, copie também um
arquivo local `wifi_profiles.json` para a raiz da placa e reinicie. Para mudar
de rede, edite esse arquivo e reinicie. Mantenha as credenciais apenas na placa
e na cópia local ignorada pelo Git.

```json
[
  {"ssid": "<primeira rede>", "password": "<senha>"},
  {"ssid": "<segunda rede>", "password": "<senha>"}
]
```

A conexão tenta os perfis na ordem configurada, por até 15 segundos cada, com
pausa de 5 segundos após falhas. Quando perde o IP, retoma as tentativas. Uma
senha vazia permite testar uma rede aberta autorizada. WPA-Enterprise (802.1X)
e autenticação em portal cativo exigem validação e suporte específicos.

O `main.py` registra as mudanças de conexão na USB serial sem exibir as
credenciais. Use Ctrl+C no terminal serial para parar o loop e voltar ao REPL.
A ponte de leituras via USB continua disponível com o firmware Arduino DEV 1.1.
Gravar MicroPython na mesma placa substitui o firmware Arduino nela. O ensaio
MicroPython nesta etapa verifica associação e reconexão Wi-Fi.
