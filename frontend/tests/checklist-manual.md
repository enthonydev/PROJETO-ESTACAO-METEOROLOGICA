# Checklist manual do dashboard

Este checklist valida comportamento visual e funcional sem tratar dados simulados como evidência física.

## Desktop

- [ ] Cabeçalho, status da estação e relógio não se sobrepõem.
- [ ] Temperatura permanece como informação visual principal.
- [ ] Umidade e pressão mantêm hierarquia secundária.
- [ ] Histórico alterna entre temperatura, umidade, pressão, qualidade do ar e luminosidade.
- [ ] Histórico é legível em 24h, 7 dias e 30 dias.
- [ ] Troca de métrica e período atualiza mínimo, média e máximo.
- [ ] Exportação CSV gera arquivo da métrica e período selecionados.
- [ ] Qualidade do ar aparece como `raw`.
- [ ] Luminosidade aparece como percentual relativo.
- [ ] Chuva sem validação quantitativa não aparece como milímetros.
- [ ] Estados de qualidade correspondem ao payload.
- [ ] Modo simulado é informado na interface.
- [ ] Atualização manual funciona sem recarregar a página.

## Cenários de demonstração

- [ ] `?demo=partial` mostra métrica ausente sem substituir por zero.
- [ ] `?demo=empty` apresenta histórico vazio sem gráfico enganoso.
- [ ] `?demo=error` apresenta falha e opção de nova tentativa.
- [ ] `?demo=invalid` rejeita contrato incompatível.

## Estados

- [ ] Durante carregamento, o painel informa que está atualizando.
- [ ] Uma resposta incompatível não é renderizada silenciosamente.
- [ ] Falha de API exibe mensagem e opção de nova tentativa.
- [ ] Perda de rede exibe estado offline quando a API real estiver habilitada.
- [ ] Métrica ausente permanece como `--` ou estado correspondente.
- [ ] Atualidade da leitura aparece sem inventar informação.

## Responsividade

- [ ] Layout permanece utilizável abaixo de 900 px.
- [ ] Layout permanece utilizável abaixo de 820 px.
- [ ] Layout permanece utilizável abaixo de 620 px.
- [ ] Layout permanece utilizável abaixo de 520 px.
- [ ] Seletores de métrica podem ser usados em tela estreita.
- [ ] Botões 24h, 7 dias e 30 dias continuam acessíveis no mobile.
- [ ] Nenhum texto ou valor ultrapassa a largura da tela.
- [ ] Rodapé permanece legível em tela estreita.

## Acessibilidade básica

- [ ] Navegação por teclado alcança seletores, atualização, exportação e nova tentativa.
- [ ] Foco dos controles permanece visível.
- [ ] Mensagens de sistema utilizam região `aria-live`.
- [ ] O gráfico possui título e descrição acessíveis.
- [ ] O painel informa estado de carregamento por `aria-busy`.
- [ ] Seletores de métrica expõem `aria-pressed`.
- [ ] Animação de carregamento respeita `prefers-reduced-motion`.
