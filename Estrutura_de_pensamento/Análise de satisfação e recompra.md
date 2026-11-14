# Análise de satisfação e recompra observada — Olist

Documento revisado em 14/11/2026. Definições gerais: [Critérios dos indicadores](Crit%C3%A9rios%20dos%20indicadores.md).

## 1. Objetivo e perguntas

Investigar duas perspectivas da experiência: as avaliações dos pedidos e a repetição de compras no histórico. Elas são apresentadas separadamente; a análise não estimou a relação entre atraso e decisão de voltar a comprar.

1. Como as notas variam entre entregas no prazo e atrasadas?
2. Como o momento registrado da resposta muda essa comparação?
3. Quantos clientes têm múltiplos pedidos, compram em dias diferentes e retornam em até 90 dias?

O público é a gestão de atendimento, experiência e relacionamento. Os resultados orientam investigações da jornada, sem comprovar efeito causal ou lealdade.

## 2. Dados e unidades

- Pedidos e prazos de `analises/entregas.py`.
- Itens de pedidos entregues de `analises/vendas.py`.
- Clientes carregados em `analises/clientes.py`, relacionados por `customer_id` e identificados como pessoa por `customer_unique_id`.
- Avaliações de `olist_order_reviews_dataset.csv`, carregadas em `analises/avaliacoes.py`.

Registro de avaliação, pedido e cliente são unidades diferentes. Consolidar antes de calcular médias ou contar pessoas evita que vários itens ou avaliações multipliquem a contribuição do mesmo pedido.

## 3. Avaliações: lógica e KPIs

### Comparação histórica

Agrupar as notas por `order_id`, calcular uma nota média para cada pedido e relacionar esse resumo à base de prazo com `one_to_one`. Cada pedido com nota tem o mesmo peso na média do grupo; pedidos sem avaliação permanecem identificados na cobertura.

| Situação final | Pedidos com nota | Nota média | Mediana | Cobertura |
|---|---:|---:|---:|---:|
| No prazo | 89.443 | 4,29 | 5 | 99,45% |
| Atrasados | 6.381 | 2,27 | 1 | 97,66% |

Dos 96.470 pedidos com prazo avaliável, **646 ficaram sem nota**. A cobertura usa todos os pedidos da situação correspondente, não somente os avaliados.

### Momento da resposta

`classificar_momento(registros)` compara `review_answer_timestamp` com o timestamp da entrega e preserva os casos não classificáveis. Respostas anteriores à entrega são divididas entre até o dia prometido e após esse dia. Para essa última divisão, o código normaliza as datas por dia; para antes/depois da entrega, compara timestamps integrais.

Dentro de cada recorte, as notas são novamente consolidadas por pedido antes da média. Na base completa há **547 pedidos com várias avaliações**. Na base com prazo, **123 pedidos aparecem em mais de um recorte temporal**; portanto, os grupos não são exclusivos.

| Pedidos finalmente atrasados | Pedidos no recorte | Registros de avaliação | Nota média por pedido |
|---|---:|---:|---:|
| Resposta antes da entrega, após o dia prometido | 4.431 | 4.445 | 1,63 |
| Resposta na entrega ou depois | 1.908 | 1.910 | 3,72 |

**70,20% dos registros associados a pedidos atrasados foram respondidos antes da entrega registrada.** O denominador desse percentual é de registros, não de pedidos. A extração conferida não apresentou ausência de datas de criação/resposta nem resposta anterior à criação; isso não confirma a semântica operacional dos registros.

### Interpretação e decisões

As notas durante a espera após o prazo foram menores nos grupos observados. A diferença direciona a investigação da jornada e da comunicação enquanto o cliente aguarda. Não demonstra melhora da nota do mesmo cliente após receber o produto.

O detalhamento também cruza faixas de atraso e momento da resposta. No grupo acima de 30 dias, apenas **sete pedidos** foram avaliados na entrega ou depois; não se deve generalizar essa média como padrão de todos os atrasos severos.

## 4. Recompra: lógica e KPIs

### Múltiplos pedidos e compras em outro dia

Partir de uma linha por pedido entregue, relacionar `customer_unique_id` e contar pedidos distintos por pessoa. A regra histórica de dois ou mais pedidos foi mantida como **múltiplos pedidos entregues**, não como prova de fidelização.

| Indicador | Clientes |
|---|---:|
| Com pelo menos um pedido entregue | 93.358 |
| Com dois ou mais pedidos entregues | 2.801 |
| Com compras em dias diferentes | 2.015 |
| Múltiplos pedidos, todos no mesmo dia | 786 |

Os 2.801 clientes de múltiplos pedidos fizeram 5.921 pedidos e somaram R$ 728.408,75 em produtos: 3,00% dos clientes e 5,51% do valor vendido. Seu ticket foi R$ 123,02 por pedido e o acumulado médio R$ 260,05 por cliente. Esse acumulado inclui a primeira compra e não é uma estimativa de valor vitalício do cliente.

### Janela de 90 dias

`calcular_recompra(pedidos, corte)` normaliza datas de compra, elimina repetição do mesmo dia por cliente e identifica a primeira data observada e a primeira posterior em outro dia. O corte é **29/08/2018**, última compra entregue observada.

```text
Elegível = pelo menos 90 dias entre a primeira compra observada e o corte
Recompra em 90 dias = elegível e segunda data distinta entre 1 e 90 dias após a primeira
Taxa = clientes elegíveis que recompraram ÷ clientes elegíveis × 100
```

Resultado: **978 de 75.387 elegíveis retornaram em outro dia dentro da janela — 1,30%**. Dia 90 entra; dia 91 não entra. Cliente com somente 30 dias observáveis fica fora do denominador. Não se exige entrega da primeira compra antes da segunda.

## 5. Uso gerencial e limitações

A análise oferece uma base para acompanhar recompra com oportunidade temporal mais comparável e distinguir novas ocasiões de compra de pedidos separados no mesmo dia. Não classifica a taxa como alta ou baixa sem uma referência comparável.

- A primeira compra é a primeira **observada de pedido entregue**, não necessariamente a primeira da vida do cliente.
- Status final, meses de borda e cobertura desigual afetam a população. A última data não comprova completude da extração.
- Os 3,00% históricos e os 1,30% em 90 dias têm definições e denominadores diferentes.
- Avaliações usam datas registradas e situação final da entrega; não comprovam o que o cliente sabia ao responder.
- Não se estimaram causalidade, lealdade ou impacto de atraso na recompra. Comparações de coortes e intervenções são possíveis evoluções, não resultados deste projeto.
- Na apresentação atual, a tabela de apoio de recompra arredonda a taxa para “1”; o valor correto permanece no texto principal (1,30%) e no CSV. Essa limitação foi documentada sem alterar o HTML.

## 6. Rastreabilidade e apresentação

As figuras de satisfação e recompra são separadas para não sugerir uma relação não analisada. O HTML apresenta notas com quantidade de pedidos e a recompra com numerador, denominador e janela.

- Código: [avaliações](../analises/avaliacoes.py), [satisfação e recompra](../analises/satisfacao_fidelizacao.py) e [gráficos](../graficos/satisfacao_fidelizacao.py).
- Evidências: [comparação histórica](../web/tabelas/satisfacao_historica.csv), [momentos](../web/tabelas/momento_avaliacoes.csv), [notas por faixa](../web/tabelas/notas_faixas.csv), [qualidade das datas](../web/tabelas/qualidade_avaliacoes.csv), [recompra](../web/tabelas/recompra.csv) e [múltiplos pedidos](../web/tabelas/multiplos_pedidos.csv).
