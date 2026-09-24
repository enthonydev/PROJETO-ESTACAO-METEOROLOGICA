# Política de Segurança

## Versões suportadas

Este é um projeto acadêmico em desenvolvimento. Durante as fases N1 e N2, somente o estado mais recente da branch `main` após revisão é considerado suportado.

## Relato de vulnerabilidades

Não publique em Issues informações que possam expor:

- senhas;
- tokens;
- chaves de API;
- credenciais de Wi-Fi;
- strings de conexão;
- dados pessoais;
- outros segredos de ambiente.

Caso uma vulnerabilidade ou credencial exposta seja identificada, comunique diretamente aos responsáveis pelo projeto antes de divulgar detalhes publicamente.

## Segredos e configuração

Credenciais reais não devem ser versionadas.

Arquivos de exemplo podem documentar apenas nomes de variáveis e valores fictícios, por exemplo:

```text
WIFI_SSID=
WIFI_PASSWORD=
MQTT_HOST=
DATABASE_URL=
WEATHER_API_KEY=
```

Credenciais utilizadas em desenvolvimento devem permanecer em configuração local ou mecanismo apropriado de secrets.

## Dependências

As dependências utilizadas pelo firmware, backend e frontend devem ser registradas e revisadas conforme o projeto evolui. Atualizações que alterem contratos ou comportamento do sistema devem passar pelo fluxo normal de revisão.

## Escopo acadêmico

Como o projeto está em desenvolvimento, limitações de segurança identificadas durante N1 e N2 devem ser registradas na documentação técnica quando forem relevantes para a arquitetura, implantação ou análise final.
