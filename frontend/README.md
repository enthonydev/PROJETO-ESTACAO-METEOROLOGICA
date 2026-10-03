# Frontend

Dashboard web da Estação Meteorológica Inteligente com ESP32.

## Estado atual

A interface pode ser desenvolvida e validada sem hardware. A versão atual opera em modo de demonstração com dados simulados enquanto os endpoints de consulta do backend não estão disponíveis.

Já estão implementados:

- painel de leitura atual;
- temperatura, umidade, pressão, qualidade do ar, luminosidade e estado de chuva;
- qualidade individual das métricas;
- histórico selecionável de temperatura, umidade, pressão, qualidade do ar e luminosidade;
- períodos de 24 horas, 7 dias e 30 dias;
- mínimo, média e máximo da série exibida;
- exportação do histórico atual em CSV;
- atualização manual;
- atualização automática a cada 60 segundos quando a aba está visível;
- estados de carregamento, simulação, erro, offline e histórico vazio;
- indicação de atualidade da última leitura;
- identificação do schema;
- localização quando latitude e longitude estiverem disponíveis;
- responsividade para desktop, tablet e celular;
- acessibilidade básica de teclado, foco, `aria-live`, `aria-busy` e redução de movimento;
- cenários de demonstração para revisão sem backend;
- testes estáticos executados no CI.

## Regras de domínio preservadas

A interface segue o contrato de telemetria v1.0:

- `air_quality_raw` permanece como valor bruto;
- luminosidade permanece relativa;
- chuva não é apresentada em milímetros sem medição quantitativa validada;
- valores ausentes não são substituídos silenciosamente por zero;
- estados de qualidade permanecem separados da medição;
- dados simulados são identificados explicitamente e não são tratados como evidência física.

## Estrutura

```text
frontend/
├── index.html
├── src/
│   ├── app.js
│   └── styles.css
└── tests/
    ├── checklist-manual.md
    └── test_frontend_static.py
```

## Execução local

A interface não exige build nem dependências JavaScript externas.

Na raiz do repositório:

```bash
python -m http.server 8000
```

Depois acesse:

```text
http://localhost:8000/frontend/
```

Também é possível abrir `frontend/index.html` diretamente no navegador.

## Cenários de demonstração

Os parâmetros abaixo permitem testar estados da interface sem alterar o código:

```text
/frontend/?demo=partial
/frontend/?demo=empty
/frontend/?demo=error
/frontend/?demo=invalid
```

- `partial`: simula uma métrica sem leitura;
- `empty`: simula histórico vazio;
- `error`: simula falha de carregamento;
- `invalid`: simula versão de contrato incompatível.

## Integração com a API

Em `src/app.js`:

```js
const USE_MOCK_DATA = true;
```

mantém o dashboard em demonstração.

Quando os endpoints REST forem implementados, altere para:

```js
const USE_MOCK_DATA = false;
```

e configure `API_BASE` quando necessário.

A interface está preparada para consumir:

```text
GET /api/v1/stations/{id}/latest
GET /api/v1/stations/{id}/measurements
```

A leitura atual é validada de forma defensiva antes da renderização. A autoridade de validação permanece no backend.

## Testes

Validação estática:

```bash
python -m pytest frontend/tests/test_frontend_static.py -q
```

O arquivo `frontend/tests/checklist-manual.md` cobre os cenários visuais, responsivos e de acessibilidade que dependem de inspeção humana.

## Direção visual

O dashboard usa linguagem visual sóbria, próxima de um painel técnico de monitoramento. A composição evita gradientes decorativos, excesso de cards, ícones sem função, glassmorphism e elementos gráficos que não comuniquem dado ou estado.

A hierarquia prioriza leitura atual, histórico, sensores complementares, qualidade dos dados e condição operacional da estação.
