# N2 — Protocolo de ensaios de rede e integração

Este documento define **testes planejados**, não resultados aprovados.

## Pré-condições

- Identificar modelo do ESP32, sensores, tensões e firmware gravado.
- Não conectar sinal de 5 V diretamente ao GPIO do ESP32. Divisor resistivo é para **sinal**, não para alimentar o aquecedor do MQ-135.
- Preservar o firmware DEV 1.1 e a ponte USB como caminho de recuperação.
- Nunca versionar senhas, SSIDs pessoais completos ou tokens.

## T-WIFI-01 — Rede pessoal

Conectar a rede autorizada, registrar IP privado mascarado e tempo de associação; transmitir 20 amostras com station_id e timestamp; verificar na API e no dashboard que são leituras reais e atuais.

## T-WIFI-02 — Rede da UNIP

Repetir o teste com autorização. Identificar se há portal cativo ou WPA-Enterprise: a conexão ESP32 comum pode não ser compatível sem implementação específica. Registrar falha ou sucesso, sem contornar controle de acesso.

## T-WIFI-03 — Rede de terceiro

Permitir configurar uma nova rede autorizada sem editar e recompilar o firmware. Confirmar que a senha não aparece em logs e que a conexão persiste após reinicialização. A implementação do provisionamento ainda é pendente.

## T-WIFI-04 — Resiliência

Desligar o AP por 60 segundos e religar. Registrar reconexão, perda de amostras, reinícios e recuperação do dashboard. Repetir 3 vezes.

## T-E2E-01 — Ponta a ponta

Verificar ESP32 → transporte → backend → armazenamento → API → dashboard com pelo menos 20 amostras identificadas; comparar timestamps e valores. A ponte USB/HTTP é caminho experimental distinto do MQTT planejado.

## Registro por teste

| Campo | Preenchimento |
|---|---|
| Data / responsável | Pendente |
| Firmware / commit | Pendente |
| Rede e autenticação (sem segredo) | Pendente |
| Evidência de IP / conexão | Pendente |
| Amostras enviadas / recebidas | Pendente |
| API e dashboard | Pendente |
| Logs e capturas | Pendente |
| Resultado | NÃO EXECUTADO |

## Entrega acadêmica

Antes dos dias 13 e 16/11/2026, conferir rubrica, atualizar matriz de rastreabilidade, registrar testes físicos e preparar roteiro de vídeo conforme instruções do professor. Não apresentar testes simulados como evidência de hardware.
