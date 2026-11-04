# Plano de fechamento N2 — 13 e 16 de novembro de 2026

**Estado: documento de planejamento, não ata de aprovação do professor.** As datas foram informadas pela equipe. A correspondência exata de atividades/entregáveis aos dias 13 e 16 depende do roteiro que será enviado ao Drive.

## 1. O que está implementado/observado

| Área | Evidência | Estado |
| --- | --- | --- |
| Montagem ESP32 + OLED + DHT22 + LDR digital + chuva digital | registro de bancada DEV 1.1 | Validado funcionalmente na bancada |
| Pressão atmosférica BMP280/BME280 | módulo não montado, requer identificação exata e solda | PENDENTE |
| Qualidade do ar MQ-135 | módulo presente, sem ligação segura verificada | PENDENTE |
| Luminosidade porcentual | DO apenas claro/escuro, AO desconectado | PENDENTE |
| Firmware Arduino DEV 1.1 | leitura e renderização OLED | Validado em bancada |
| Firmware integrado N2 Wi-Fi + NTP + MQTT | código nesta branch, com configurações locais | Preparado; **não compilado nem testado na placa** |
| Backend FastAPI | API REST, testes backend GitHub Actions | Validado em software |
| Broker MQTT + consumer + PostgreSQL | integração com publicador sintético no CI | Validado em software e runtime CI; ESP32 real pendente |
| Dashboard Clima iOS | UI ligada à API, testes estáticos CI | Validado em software; leitura de ESP32 real no navegador pendente |
| Ponte serial USB | parser e POST HTTP com testes automatizados | Implementado; roundtrip físico pendente |
| Documentação da N1 | relatório N1, requisitos, ADRs e matriz histórica | Concluído como entrega anterior |
| Documentação da N2 | relatório técnico e evidências de bancada iniciais | Em andamento; nova rubrica/padrão do vídeo pendentes |

## 2. Checklist para entrega física e acadêmica

### Componentes
- [x] ESP32 inicializa e sensores DHT22, chuva, LDR digitais, OLED respondem.
- [ ] Fotografar a montagem e confirmar continuidade das ligações, alimentação e reinício com LDR claro/escuro.
- [ ] Confirmar se módulo de pressão é **BMP280 ou BME280** e sua tensão/pinagem olhando a placa real; soldar pinos com equipamento adequado, inspecionar curtos antes de energizar.
- [ ] Integrar pressão na I2C (SDA=21, SCL=22); verificar se endereço 0x76/0x77 e VCC são compatíveis; testar OLED simultaneamente.
- [ ] Conferir a tensão de alimentação, corrente e nível de saída AO do **MQ-135**; não energizar via resistor em série; usar alimentação 5 V compatível e divisor para AO **se medido necessário**.
- [ ] Escolher GPIO **ADC1 acessível** para MQ-135; registrar fiação. Saída do divisor AO deve ficar sempre dentro do limite da entrada do ESP32, inclusive no pico.
- [ ] Fazer teste de LDR analógico relativo em ADC1 com extremos escuro/claro registrados; não chamar DO de percentual.
- [ ] Registar GND comum, desvios, datasheets, fotos e leituras de multímetro; nunca medir resistência com energia.
- [ ] Repetir os testes dos sensores em conjunto, 15–30 minutos mínimos de observação; tempo oficial de stress deve seguir rubrica do professor.

### Rede/telemetria
- [ ] Compilar firmware N2 em IDE Arduino e validar que baseline local continua funcionando.
- [ ] Configurar `local_config.h` na máquina e **não publicar senhas**.
- [ ] Testar Wi-Fi 2,4 GHz com credenciais autorizadas na rede 1 (residencial), registrar IP, duração, perda e reconexão.
- [ ] Testar rede da UNIP, registrar SSID/tipo de autenticação. Se 802.1X, captive portal, isolamento de clientes ou bloqueio de portas, documentar e adaptar ambiente; `WiFi.begin(ssid,password)` isoladamente **não garante** acesso.
- [ ] Testar uma terceira rede **com autorização do responsável**; repetir reconexão e troca de rede.
- [ ] Registrar resultado de desligar/restabelecer uma rede sem reiniciar o ESP32, conforme orientação do professor.
- [ ] Sincronizar NTP e validar timestamp UTC real, sem data inventada.
- [ ] Preparar broker MQTT com autenticação, PostgreSQL e worker; confirmar publicação **pelo ESP32 real**.
- [ ] Verificar persistência, API e dashboard usando leitura mais recente da estação real; guardar captura de resposta e tela.
- [ ] Executar `python scripts/check_live_station.py`; conservar a saída real.

### Entrega
- [ ] Receber os documentos adicionais e o roteiro do vídeo no Drive; confirmar critérios e datas.
- [ ] Atualizar `hardware/pinout.md`, `hardware/plano-testes.md`, rastreabilidade N2 e ADR pertinente após montagem final.
- [ ] Escrever relatório N2 com logs, fotos, medições, falhas encontradas e pendências honestas.
- [ ] Gravar vídeo mostrando hardware, OLED, troca de rede, broker, leituras reais e dashboard, **somente segundo rubrica que será enviada**.
- [ ] Executar CI e revisão de PR; preparar release/tag e pacote de submissão na versão efetivamente demonstrada.
- [ ] Confirmar checklist e conteúdos específicos do dia **13/11** e do dia **16/11** com roteiro do professor.

## 3. Riscos e decisões

- A ADR-002 já eliminou o **BME280 adicional**, mas exige **BMP280 para pressão** e **MQ-135 para qualidade do ar**. Não mudar esse escopo sem aprovação.
- O **sensor de chuva** oferece detecção molhado/seco; não há medição de precipitação em milímetros.
- O **MQ-135** geralmente requer aquecedor a 5 V. Divisor resistivo serve à **saída analógica**, não à alimentação do módulo. Exemplo puramente teórico para saída até 5 V: 10 kΩ em série com AO e 15 kΩ entre nó ADC e GND limita o nó a ~3,0 V; confirmar resistores e níveis com multímetro **antes** de conectar ao ESP32. Respeitar dissipação e tolerâncias, e priorizar projeto validado.
- O módulo **BMP280/BME280** deve ser identificado por marcação/esquema, não pela cor da placa.
- GPIO5 (LDR digital) é pino de strapping e pode afetar boot.
- Nunca cadastrar credenciais de terceiros ou da UNIP no repositório, no vídeo ou nas evidências públicas.
- A validação em CI demonstra somente software sintético; **não marca hardware físico ou stress Wi-Fi como aprovado**.
