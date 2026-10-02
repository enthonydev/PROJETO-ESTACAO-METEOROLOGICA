# Checklist manual do dashboard

Este checklist valida comportamento visual e funcional sem tratar dados simulados como evidência física.

## Desktop

- [ ] Cabeçalho, status da estação e relógio não se sobrepõem.
- [ ] Temperatura permanece como informação visual principal.
- [ ] Umidade e pressão mantêm hierarquia secundária.
- [ ] Histórico de temperatura é legível em 24h, 7 dias e 30 dias.
- [ ] Troca de período atualiza mínimo, média e máximo.
- [ ] Qualidade do ar aparece como `raw`.
- [ ] Luminosidade aparece como percentual relativo.
- [ ] Chuva sem validação quantitativa não aparece como milímetros.
- [ ] Estados de qualidade correspondem ao payload.
- [ ] Modo simulado é informado na interface.

## Estados

- [ ] Durante carregamento, o painel informa que está atualizando.
- [ ] Uma resposta incompatível não é renderizada silenciosamente.
- [ ] Falha de API exibe mensagem e opção de nova tentativa.
- [ ] Perda de rede exibe estado offline quando a API real estiver habilitada.
- [ ] Histórico vazio apresenta mensagem própria, sem gráfico enganoso.
- [ ] Métrica ausente permanece como `--` ou estado correspondente, sem substituição por zero.

## Responsividade

- [ ] Layout permanece utilizável abaixo de 820 px.
- [ ] Layout permanece utilizável abaixo de 520 px.
- [ ] Botões 24h, 7 dias e 30 dias continuam acessíveis no mobile.
- [ ] Nenhum texto ou valor ultrapassa a largura da tela.
- [ ] Rodapé permanece legível em tela estreita.

## Acessibilidade básica

- [ ] Navegação por teclado alcança os controles de período.
- [ ] Foco dos botões permanece visível.
- [ ] Mensagens de sistema utilizam região `aria-live`.
- [ ] O gráfico possui descrição acessível.
- [ ] O painel informa estado de carregamento por `aria-busy`.
- [ ] Animação de carregamento respeita `prefers-reduced-motion`.
