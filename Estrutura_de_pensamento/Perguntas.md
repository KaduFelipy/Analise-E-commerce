# Perguntas de negócio e caminho da análise — Olist

Revisão documental: 14/11/2026. Público: gestão comercial, logística, atendimento e relacionamento. As perguntas abaixo estão ligadas aos cálculos implementados; causas e ações operacionais permanecem em investigação.

## 1. Como uma pergunta se transforma em evidência

Pergunta de gestão → população e unidade de análise → relacionamento das tabelas → KPI e comparação → validação → gráfico/tabela → significado → próxima investigação.

Os denominadores e períodos estão nos [Critérios dos indicadores](Crit%C3%A9rios%20dos%20indicadores.md). Cada documento tem seus dados, lógica, resultados, contribuição gerencial e limites.

## 2. Vendas

- Como o valor dos produtos, os pedidos e o ticket variaram mês a mês?
- Quais categorias compõem a diferença novembro/dezembro de 2017?
- Como itens por pedido e preço médio por item ajudam a descrever o ticket?

**Evidência implementada:** queda de 26,50%; três categorias somam reduções equivalentes a 38,64% da queda líquida. **Uso:** escolher produtos/categorias para investigar. Disponibilidade, estoque e campanhas não foram demonstrados como causas.

Detalhes: [Análise de vendas](An%C3%A1lise%20de%20desempenho%20de%20vendas%20-%20Olist.md).

## 3. Prazos e severidade

- Qual a frequência e duração dos atrasos entre pedidos entregues com datas válidas?
- Quais destinos e meses concentram quantidade e taxa elevadas?
- Como os intervalos da espera diferem entre entregas no prazo, atrasadas e acima de 30 dias no episódio escolhido?

**Evidência implementada:** taxa geral de 6,77%; RJ fevereiro/março de 2018 com 597 atrasos em 1.743 avaliáveis; intervalos segmentados. **Uso:** selecionar episódios para examinar registros de transporte e ocorrências, sem atribuir responsabilidade antecipadamente.

Detalhes: [Análise de prazos](An%C3%A1lise%20de%20prazos%20de%20entrega%20-%20Olist.md).

## 4. Distribuição geográfica

- Onde se concentram clientes e valor vendido?
- Como ticket, frete médio, proporção de frete e atraso se combinam nos destinos de maior exposição comercial?

**Evidência implementada:** totais estaduais e seleção dos cinco maiores estados por valor dos produtos, com referência nacional pelos totais. **Uso:** distinguir concentração comercial e pontos para investigação logística. Frete registrado não é custo comprovado.

Detalhes: [Análise geográfica](An%C3%A1lise%20da%20distribui%C3%A7%C3%A3o%20geogr%C3%A1fica.md).

## 5. Vendedores

- Quais vendedores estão associados a mais atrasos, e qual é o tamanho da base?
- Como a comparação muda ao selecionar vendedor único e a mesma UF/trimestre?

**Evidência implementada:** ranking histórico, células mensais e complemento de dez vendedores em abril/2017–junho/2018, excluindo o próprio vendedor da referência trimestral. **Uso:** selecionar grupos para investigação contextualizada; não definir os “piores” por taxas pequenas ou não ajustadas.

Detalhes: [Análise dos vendedores](An%C3%A1lise%20de%20entregas%20e%20desempenho%20dos%20vendedores.md).

## 6. Avaliações e recompra

- Como notas variam por situação final e momento registrado da resposta?
- Quantos clientes têm múltiplos pedidos, compram em dias diferentes e retornam em 1–90 dias com acompanhamento elegível?

**Evidência implementada:** entre finalmente atrasados, notas 1,63 durante a espera após o prazo e 3,72 na entrega/depois; recompra de 978/75.387 elegíveis (1,30%). **Uso:** investigar a jornada e estruturar acompanhamento de recompra. Não se analisou o efeito de atraso na recompra nem a mudança individual das notas.

Detalhes: [Satisfação e recompra](An%C3%A1lise%20de%20satisfa%C3%A7%C3%A3o%20e%20recompra.md).

## 7. Pagamentos

- Como os pedidos entregues foram pagos?
- Como média, mediana e volume variam por parcelas e categoria no recorte de cartão?

**Evidência implementada:** cartão concentra 78,46% do valor pago; relógios e presentes em oito parcelas tem 687 pedidos no complemento de categoria única. **Uso:** investigar composição comercial antes de avaliar condições de pagamento; não comprovar efeito de mais parcelas nas vendas.

Detalhes: [Análise de pagamentos](An%C3%A1lise%20de%20pagamentos.md).

## 8. Limite das decisões e próximos passos

As três prioridades finais são a investigação do episódio logístico do RJ, dos produtos nas categorias da queda comercial e das avaliações durante a espera. Recompra e pagamentos são perspectivas próprias, sem ligação causal demonstrada com esses episódios.

Custos, margem, transportadora, ocorrências, estoque e campanhas seriam informações adicionais para avaliar causas e viabilidade. Não há metas operacionais inventadas, previsão ou impacto real de intervenção medido. A versão atual foi encerrada pelo usuário; esses próximos passos são possibilidades.
