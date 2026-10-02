# Frontend

Dashboard web da Estação Meteorológica Inteligente com ESP32.

## Estado atual

A interface pertence à continuidade do projeto após a N1 e ainda opera com dados simulados enquanto os endpoints de consulta do backend não estão disponíveis.

A versão atual já trata estados de carregamento, erro, ausência de histórico e perda de conexão, além de diferenciar visualmente o modo de demonstração da futura operação conectada à API.

A interface segue o contrato de telemetria v1.0 e preserva suas limitações:

- `air_quality_raw` é exibido como leitura bruta;
- luminosidade é apresentada como percentual relativo;
- chuva não é exibida em milímetros quando não há medição quantitativa validada;
- estados de qualidade são apresentados separadamente;
- dados simulados são identificados explicitamente e não são tratados como evidência física.

## Estrutura

```text
frontend/
├── index.html
├── src/
│   ├── app.js
│   └── styles.css
└── tests/
    └── checklist-manual.md
```

## Execução local

A interface não exige build.

É possível abrir `frontend/index.html` diretamente no navegador ou utilizar um servidor HTTP local simples.

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

mantém a interface em modo de demonstração.

Quando os endpoints REST estiverem disponíveis, altere para:

```js
const USE_MOCK_DATA = false;
```

e configure `API_BASE` quando necessário.

A interface está preparada para consumir:

```text
GET /api/v1/stations/{id}/latest
GET /api/v1/stations/{id}/measurements
```

O payload da leitura atual é validado de forma defensiva antes da renderização. A validação completa continua sendo responsabilidade do backend.

## Estados de interface

A versão atual possui tratamento explícito para:

- carregamento;
- modo de demonstração;
- operação online;
- falha de API;
- navegador offline;
- histórico vazio;
- métricas ausentes;
- estados `ok`, `suspect`, `invalid` e `error`.

## Direção visual

O dashboard usa linguagem visual sóbria, inspirada em instrumentos e painéis de monitoramento. A interface evita gradientes decorativos, excesso de cards, ícones sem função e elementos visuais que não contribuam para leitura ou estado do sistema.

A hierarquia prioriza:

1. leitura atual;
2. histórico;
3. sensores complementares;
4. qualidade dos dados;
5. estado operacional da estação.
