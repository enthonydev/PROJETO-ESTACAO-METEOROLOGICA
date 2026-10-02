# Frontend

Dashboard web da Estação Meteorológica Inteligente com ESP32.

## Estado atual

A primeira interface funcional do projeto foi iniciada após o fechamento da N1. Esta etapa pertence à continuidade do projeto e ainda utiliza dados simulados para permitir desenvolvimento e validação visual antes da integração completa com o backend.

A interface segue o contrato de telemetria v1.0 e preserva suas limitações:

- `air_quality_raw` é exibido como leitura bruta;
- luminosidade é apresentada como percentual relativo;
- chuva não é exibida em milímetros quando não há medição quantitativa validada;
- estados de qualidade são apresentados separadamente;
- dados simulados não são tratados como evidência física.

## Estrutura

```text
frontend/
├── index.html
└── src/
    ├── app.js
    └── styles.css
```

## Execução local

A interface não exige build.

Abra `frontend/index.html` diretamente no navegador ou utilize um servidor HTTP local simples.

Exemplo:

```bash
python -m http.server 8000
```

Depois acesse:

```text
http://localhost:8000/frontend/
```

## Integração com a API

Em `src/app.js`, a constante:

```js
const USE_MOCK_DATA = true;
```

mantém a interface em modo de simulação.

Quando os endpoints REST estiverem disponíveis, altere para:

```js
const USE_MOCK_DATA = false;
```

e configure `API_BASE` quando necessário.

A interface foi preparada para consumir:

```text
GET /api/v1/stations/{id}/latest
GET /api/v1/stations/{id}/measurements
```

## Direção visual

O dashboard utiliza uma linguagem visual sóbria, inspirada em instrumentos e painéis de monitoramento, evitando elementos decorativos sem função. A hierarquia prioriza leitura atual, histórico e estado dos sensores.
