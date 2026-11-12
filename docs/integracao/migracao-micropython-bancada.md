# Migrar a bancada para MicroPython

Pacote preparado em 12/11/2026. Destino: ESP32 clássico WROOM/DevKit, porta habitual COM7. Não usar a imagem ESP32_GENERIC em S2, S3 ou C3.

## O que já está pronto

Firmware integrado, driver OLED incluído, scanner I2C real, leituras DHT22, chuva e LDR digitais, pressão DEMO, seleção de várias redes e reconexão automática. O programa continua lendo e desenhando sem Wi-Fi. Formato do DHT no Serial preservado para a ponte USB.

O instalador verifica SHA-256 da imagem oficial MicroPython 1.26.1, solicita credenciais localmente, lê uma cópia completa da flash **antes de apagar**, grava o runtime e copia os arquivos. Se o backup falhar, interrompe antes de apagar. Guarde `backups/` fora da pasta se for excluir o pacote. A restauração é exclusiva desta mesma placa.

## Executar no Windows

1. Extraia o ZIP inteiro em uma pasta. Tenha Python 3.10+ instalado com o launcher `py`; as ferramentas serão instaladas automaticamente e precisam de internet na primeira execução.
2. Conecte o ESP32 pelo mesmo cabo USB de dados. Feche Arduino IDE, Monitor Serial, Thonny e qualquer ponte que esteja usando COM7.
3. Abra o PowerShell na pasta extraída e execute:

```powershell
powershell -ExecutionPolicy Bypass -File .\MIGRAR_ESP32.ps1 -Porta COM7
```

Digite SSID e senha apenas no seu notebook. Adicione uma segunda rede, como hotspot 2,4 GHz, se desejar. Enter no SSID encerra a lista; sem redes o protótipo funciona offline. Não publique `wifi_profiles.json`, backups ou senhas. Redes que exigem login por navegador/802.1X precisam de configuração adicional; use Wi-Fi pessoal 2,4 GHz no ensaio.

Se parar em `Connecting...`, mantenha BOOT pressionado durante a conexão e solte quando iniciar a leitura/gravação. Não desconecte durante backup/gravação. Qualquer falha deve ser lida antes de repetir. Se o backup não puder ser feito, o script não avançará para o apagamento.

## Montagem preservada

| Função | GPIO / ligação |
| --- | --- |
| DHT22 dados | GPIO16 |
| Chuva digital | GPIO17, ativo LOW |
| LDR digital | GPIO5, HIGH = escuro |
| OLED SDA / SCL | GPIO21 / GPIO22 |
| OLED I2C | 0x3C, 128 × 64 |
| Alimentação e terra | Manter a montagem atual, sem mudar de tensão |
| Módulo 280 | Não é usado para pressão neste firmware |

Não é necessário reposicionar componentes para trocar a linguagem. Mau contato em VCC/GND continua sendo um problema físico: a recuperação automática da OLED não corrige um jumper defeituoso.

## Conferência rápida depois da gravação

Abra somente um leitor USB por vez:

```powershell
powershell -ExecutionPolicy Bypass -File .\VER_USB.ps1 -Porta COM7
```

No terminal, Ctrl+] encerra o monitor. Para interromper o programa e acessar o REPL, use Ctrl+C; Ctrl+D reinicia o MicroPython. Não deixe esse monitor aberto ao iniciar o dashboard.

- Scanner: deve registrar os endereços que realmente responderem. No último ensaio Arduino havia somente `0x3C`; não é esperado inventar `0x76` ou `0x77`.
- DHT: linha `Temperatura: ... C | Umidade: ... %` aproximadamente a cada 2 s.
- OLED: temperatura, umidade, `P DEMO`, chuva, luz e `W:S` conectado / `W:N` offline.
- Pressão: primeiro valor após cerca de 2 s, entre 1022,0 e 1024,0 hPa; muda após 200 intervalos de 2 s, cerca de 6 min 40 s. É gerada pelo código, não medida.
- Wi-Fi: deve aparecer `[WIFI] Conectado. IP: ...`. Desligue a rede e confira se DHT/OLED continuam atualizando; religue e aguarde a reconexão. Com dois perfis, teste também a troca de rede.
- USB: sem depender de internet, confira logs, Ctrl+C e reinício com Ctrl+D.

Registre o resultado físico antes de considerar a migração validada ou integrar a branch principal.

## Dashboard com os dados do protótipo

Feche o monitor USB e execute:

```powershell
powershell -ExecutionPolicy Bypass -File .\ABRIR_DASHBOARD.ps1 -Porta COM7
```

O comando instala dependências, abre dois terminais — API e ponte USB — e a página da estação. Aguarde a API iniciar; a ponte tenta novamente se ela ainda não estiver pronta. Atualização visual a cada 10 s. Encerre os dois terminais com Ctrl+C ao terminar.

Temperatura e umidade vêm das linhas reais do DHT. Sem PostgreSQL, o histórico é temporário e se perde ao encerrar a API. Pressão DEMO permanece apenas na OLED/Serial; chuva digital não mede milímetros, e LDR digital não mede porcentagem. MQTT do ESP32 não foi adicionado nesta etapa: conectar ao Wi-Fi e enviar telemetria ao broker são verificações distintas.

## Atualizar sem apagar novamente

Depois da primeira instalação, para atualizar arquivos ou redes:

```powershell
powershell -ExecutionPolicy Bypass -File .\MIGRAR_ESP32.ps1 -Porta COM7 -SomenteArquivos
```

## Recuperar o estado anterior

Feche todos os monitores. Localize o arquivo `.bin` dentro de `backups/` e rode, substituindo o caminho pelo arquivo real:

```powershell
.\.tools-venv\Scripts\python.exe tools/migrate_esp32.py --port COM7 --restore backups\PASTA_DO_BACKUPlash-original.bin
```

Confira o nome exato do arquivo no diretório; o instalador imprime esse caminho. A restauração valida o checksum do backup antes de escrever. Outra alternativa é regravar seu sketch Arduino original pelo IDE.

## Evidências e fontes

Os testes automatizados cobrem agendamento, pressão DEMO, falhas/reinício da OLED, falhas do DHT, USB, perfis e reconexão, além da ordem backup → apagamento → gravação. A execução na placa permanece pendente até o checklist acima.

- MicroPython ESP32: https://docs.micropython.org/en/v1.26.0/esp32/quickref.html
- Imagem oficial: https://micropython.org/download/ESP32_GENERIC/
- mpremote: https://docs.micropython.org/en/latest/reference/mpremote.html
- esptool: https://docs.espressif.com/projects/esptool/en/release-v4/esp32/esptool/basic-commands.html
