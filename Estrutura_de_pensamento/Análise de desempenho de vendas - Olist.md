> Documento revisado em 14/11/2026. Preserva a lógica da análise inicial e incorpora os recortes implementados na versão final. Definições comuns em [Critérios dos indicadores](Crit%C3%A9rios%20dos%20indicadores.md); histórico de implementação em [Entrega da evolução](Entrega%20da%20evolu%C3%A7%C3%A3o.md).

# Análise de desempenho de vendas — Olist

## 1. Objetivo

Investigar a evolução mensal do valor vendido, a participação das categorias e a variação do ticket médio.

A análise busca compreender como o valor dos produtos em pedidos entregues se relaciona com a quantidade de pedidos e o valor médio de cada compra.

## 2. Público e decisões apoiadas

**Público:** gestão comercial e responsáveis pelo acompanhamento do desempenho de vendas.

**Decisões apoiadas:** identificar períodos de maior oscilação, acompanhar categorias relevantes e distinguir mudanças no volume de pedidos de mudanças no ticket médio.

Os resultados orientam investigações, mas não demonstram, isoladamente, o efeito de promoções, campanhas, preços ou datas comemorativas.

## 3. Perguntas da análise

1. Como as vendas evoluíram mês a mês?
2. Quais categorias mais contribuem para o valor total vendido?
3. Como o ticket médio varia ao longo dos meses?

## 4. Dados utilizados

Fonte: [Brazilian E-Commerce Public Dataset by Olist — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

Foram utilizadas três tabelas:

| Tabela | Finalidade |
|---|---|
| `olist_orders_dataset.csv` | Identificar pedidos, status e datas de compra |
| `olist_order_items_dataset.csv` | Identificar os itens dos pedidos e seus preços |
| `olist_products_dataset.csv` | Identificar a categoria de cada produto |

Principais campos:

| Campo | Significado |
|---|---|
| `order_id` | Identificador do pedido |
| `order_status` | Status registrado do pedido |
| `order_purchase_timestamp` | Data e horário da compra |
| `order_item_id` | Identificador do item dentro do pedido |
| `product_id` | Identificador do produto |
| `price` | Preço do item, sem frete |
| `product_category_name` | Categoria cadastrada do produto |

### Unidade de análise

Na tabela de pedidos, cada linha representa um pedido.

Na tabela de itens, cada linha representa um item de um pedido. Como um pedido pode conter vários itens, seu `order_id` pode aparecer várias vezes nessa tabela.

A combinação de `order_id` e `order_item_id` identifica cada item dentro do pedido.

Essa diferença foi considerada para evitar que a quantidade de itens fosse interpretada como quantidade de pedidos.

## 5. Definições e critérios

| Critério | Definição utilizada |
|---|---|
| Pedidos considerados | Somente pedidos com status `delivered` |
| Valor vendido | Soma dos preços dos itens, sem frete |
| Mês de referência | Mês da compra, identificado por `order_purchase_timestamp` |
| Quantidade de pedidos | Contagem de `order_id` distintos |
| Ticket médio | Valor vendido dividido pela quantidade de pedidos distintos |
| Participação de categoria | Valor vendido da categoria dividido pelo valor total vendido |

O indicador representa o **valor dos produtos em pedidos entregues**. Ele não deve ser interpretado como lucro ou receita líquida.

A seleção de vendas foi feita independentemente da análise de entregas. Pedidos entregues sem data real de entrega foram mantidos, pois essa data não é necessária para os indicadores de vendas.

## 6. Investigação da qualidade dos dados

### Pedidos e itens

Foram encontrados:

| Verificação | Resultado |
|---|---:|
| Identificadores de pedido ausentes | 0 |
| Status de pedido ausentes | 0 |
| Datas de compra ausentes | 0 |
| Identificadores de pedido repetidos na tabela de pedidos | 0 |
| Campos necessários ausentes nos itens | 0 |
| Combinações de `order_id` e `order_item_id` repetidas | 0 |
| Itens com preço igual a zero ou negativo | 0 |

A coluna `price` foi reconhecida como numérica, do tipo `float64`.

Na tabela completa de itens, os preços variaram entre **R$ 0,85 e R$ 6.735,00**. Um preço elevado não foi tratado automaticamente como erro.

### Relacionamento entre pedidos e itens

Foram selecionados **96.478 pedidos entregues**.

Todos possuíam itens correspondentes. Após a junção:

| Resultado | Quantidade |
|---|---:|
| Pedidos distintos | 96.478 |
| Itens vendidos | 110.197 |
| Pedidos entregues sem itens correspondentes | 0 |

O valor total dos produtos foi de **R$ 13.221.498,11**, sem frete.

A junção foi validada como vários itens para um pedido, evitando multiplicação causada por identificadores repetidos na tabela de pedidos.

### Produtos e categorias

Na tabela de produtos, foram encontrados:

| Verificação | Resultado |
|---|---:|
| Identificadores de produto ausentes | 0 |
| Identificadores de produto repetidos | 0 |
| Produtos sem categoria | 610 |

Após relacionar os produtos aos itens vendidos:

| Verificação | Resultado |
|---|---:|
| Itens vendidos sem produto correspondente | 0 |
| Itens vendidos sem categoria | 1.537 |

Os itens sem categoria foram preservados no grupo **“Sem categoria”**.

O total vendido por categoria foi reconciliado com o total vendido, utilizando comparação com tolerância para pequenas diferenças de representação numérica.

### Cobertura temporal

A inspeção das primeiras e últimas compras de cada mês mostrou:

- Registros concentrados em poucos dias nos meses disponíveis de 2016.
- Ausência de novembro de 2016 na tabela mensal.
- Janeiro de 2017 com primeira compra registrada em 05/01.
- Agosto de 2018 com última compra registrada em 29/08.

Para a comparação mensal principal, foi adotado o período de **fevereiro de 2017 a julho de 2018**.

Nesse intervalo, havia compras registradas no primeiro e no último dia de cada mês. Isso favorece a comparação, mas não comprova a completude da extração.

Todos os meses foram preservados na tabela original. Os totais gerais e a participação das categorias utilizam toda a base selecionada de pedidos entregues.

## 7. Indicadores e resultados

### 7.1. Evolução mensal do valor vendido

O valor vendido mensal foi calculado pela soma dos preços dos itens, agrupados pelo ano e mês da compra.

```text
Valor vendido mensal = soma dos preços dos itens
                       dos pedidos entregues comprados no mês
```

A variação mensal foi calculada em relação ao mês anterior:

```text
Variação mensal (%) =
(valor do mês atual ÷ valor do mês anterior − 1) × 100
```

O primeiro mês do recorte ficou sem variação, pois não possui um mês anterior dentro da seleção.

Destaques do período comparável:

| Destaque | Mês | Resultado |
|---|---|---:|
| Maior crescimento mensal | Março de 2017 | +53,36% |
| Maior queda mensal | Dezembro de 2017 | −26,50% |
| Maior valor vendido | Novembro de 2017 | R$ 987.765,37 |
| Maior quantidade de pedidos | Novembro de 2017 | 7.289 |

Março de 2017 apresentou o maior crescimento relativo ao mês anterior, mas novembro de 2017 atingiu o maior valor vendido.

Em dezembro de 2017, houve queda de 26,50% em relação ao pico de novembro. Os dados descrevem esse movimento sem demonstrar sua causa.

### 7.2. Participação das categorias

A participação de cada categoria foi calculada sobre o valor total vendido da base selecionada:

```text
Participação da categoria (%) =
valor vendido da categoria ÷ valor total vendido × 100
```

As dez categorias com maior valor vendido foram:

| Categoria | Valor vendido | Itens vendidos | Participação |
|---|---:|---:|---:|
| Beleza e saúde | R$ 1.233.131,72 | 9.465 | 9,33% |
| Relógios e presentes | R$ 1.166.176,98 | 5.859 | 8,82% |
| Cama, mesa e banho | R$ 1.023.434,76 | 10.953 | 7,74% |
| Esporte e lazer | R$ 954.852,55 | 8.431 | 7,22% |
| Informática e acessórios | R$ 888.724,61 | 7.644 | 6,72% |
| Móveis e decoração | R$ 711.927,69 | 8.160 | 5,38% |
| Utilidades domésticas | R$ 615.628,69 | 6.795 | 4,66% |
| Cool stuff | R$ 610.204,10 | 3.718 | 4,62% |
| Automotivo | R$ 578.966,65 | 4.140 | 4,38% |
| Brinquedos | R$ 471.286,48 | 4.030 | 3,56% |

**Beleza e saúde liderou em valor vendido.** Entre as dez categorias apresentadas, cama, mesa e banho teve a maior quantidade de itens.

Isso demonstra que maior quantidade de itens não significa necessariamente maior valor vendido.

O grupo **“Sem categoria”** reuniu:

- **1.537 itens.**
- **R$ 170.726,63 em valor vendido.**
- **1,29% do valor total vendido.**

### 7.3. Ticket médio mensal

O ticket médio foi calculado dividindo o valor vendido pela quantidade de pedidos distintos em cada mês.

```text
Ticket médio mensal =
valor vendido no mês ÷ quantidade de pedidos distintos no mês
```

O denominador utiliza pedidos, e não itens. Um pedido com vários produtos continua contando apenas uma vez.

No período de fevereiro de 2017 a julho de 2018:

| Destaque | Mês | Ticket médio |
|---|---|---:|
| Maior ticket médio | Abril de 2017 | R$ 147,92 |
| Menor ticket médio | Julho de 2017 | R$ 124,38 |
| Ticket do mês com maior valor vendido | Novembro de 2017 | R$ 135,51 |

Comparação entre abril e julho de 2017:

| Indicador | Abril de 2017 | Julho de 2017 |
|---|---:|---:|
| Valor vendido | R$ 340.669,68 | R$ 481.604,52 |
| Quantidade de pedidos | 2.303 | 3.872 |
| Ticket médio | R$ 147,92 | R$ 124,38 |

Julho apresentou maior valor vendido que abril, apesar do ticket menor, porque teve mais pedidos.

A relação entre os indicadores é:

```text
Valor vendido = quantidade de pedidos × ticket médio
```

## 8. Storytelling dos resultados

### O desempenho envolve valor e volume

A base selecionada reuniu **96.478 pedidos entregues**, com **110.197 itens** e **R$ 13.221.498,11** em valor dos produtos, sem frete.

Para compreender esse desempenho, foi necessário observar quanto foi vendido, quantos pedidos ocorreram e qual foi o valor médio de cada pedido.

### O maior crescimento não foi o maior valor vendido

Março de 2017 apresentou o maior crescimento mensal do período comparável, de 53,36%.

Novembro de 2017 atingiu o maior valor vendido, com R$ 987.765,37 e 7.289 pedidos. Em dezembro, houve queda de 26,50% em relação a novembro.

Esses resultados distinguem crescimento relativo de volume absoluto e não comprovam o efeito de campanhas ou datas comemorativas.

### Um ticket menor pode acompanhar um valor vendido maior

Abril de 2017 apresentou ticket médio de R$ 147,92, superior ao de julho, de R$ 124,38.

Apesar disso, julho teve maior valor vendido porque reuniu mais pedidos.

Novembro também liderou em valor vendido sem apresentar o maior ticket médio. Por isso, uma redução no ticket não deve ser interpretada isoladamente como piora nas vendas.

### As categorias contribuem de formas diferentes

Beleza e saúde apresentou a maior participação no valor vendido, com 9,33%.

Cama, mesa e banho teve mais itens vendidos entre as dez categorias apresentadas, mas ficou em terceiro em valor.

A participação das categorias indica sua contribuição para o valor vendido, sem demonstrar margem ou lucro.

### A orientação para a gestão

Diante de uma mudança no valor vendido, a primeira leitura deve separar:

- Mudança na quantidade de pedidos.
- Mudança no ticket médio.
- Mudança simultânea nos dois indicadores.

Também é importante acompanhar as categorias de maior participação e melhorar o cadastro dos produtos sem classificação.

Essas leituras orientam a investigação, sem atribuir causas ainda não demonstradas pelos dados.

## 9. Limitações

- A análise utiliza uma base histórica e não representa necessariamente a operação atual.
- Foram considerados somente pedidos com status `delivered`.
- O valor vendido não inclui frete e não representa lucro ou receita líquida.
- Os totais gerais e as categorias utilizam toda a base selecionada; a comparação mensal principal utiliza fevereiro de 2017 a julho de 2018.
- A presença de compras no primeiro e no último dia do mês não comprova a completude dos registros.
- Não foram comparados anos completos, pois 2018 não possui todos os meses disponíveis.
- As causas das oscilações mensais não foram investigadas.
- A contribuição das categorias foi medida especificamente na comparação novembro/dezembro de 2017; a decomposição não foi generalizada a todas as variações mensais.
- As diferenças de ticket podem estar relacionadas a preços, quantidade de itens por pedido ou composição dos produtos, mas essas hipóteses não foram testadas.
- Os itens sem categoria foram preservados, mas sua classificação original permanece desconhecida.
- Os valores foram processados como `float64`; a reconciliação tolera pequenas diferenças de representação numérica, sem constituir auditoria contábil.

## 10. Aprofundamento: o que compõe a queda de novembro/dezembro?

### Contexto e lógica

O resultado mensal mostrou a queda, mas ainda era necessário localizar sua composição. A análise passou de “quanto variou?” para “quais categorias participaram dessa diferença?”. A função `calcular_contribuicoes(dados)`, em `analises/vendas.py`, agrupa o valor por categoria/mês e calcula dezembro menos novembro. Categorias sem venda em um dos dois meses recebem zero naquele mês; “Sem categoria” permanece incluída.

| Indicador | Novembro/2017 | Dezembro/2017 | Variação |
|---|---:|---:|---:|
| Valor dos produtos | R$ 987.765,37 | R$ 726.033,19 | −26,50% |
| Pedidos | 7.289 | 5.513 | −24,37% |
| Ticket médio | R$ 135,51 | R$ 131,69 | −2,82% |

A queda líquida foi de **R$ 261.732,18**. Cama, mesa e banho; informática e acessórios; e móveis e decoração somaram **R$ 101.142,30 em reduções**, equivalentes a **38,64% da queda líquida**. A proporção usa a queda após as compensações das categorias que cresceram, e não a soma apenas das reduções. Não se somam as variações percentuais de pedidos e ticket como contribuições aditivas.

O ticket também foi decomposto pela identidade `ticket = itens por pedido × preço médio por item`. Entre novembro e dezembro, os itens por pedido passaram de aproximadamente 1,16 para 1,12, enquanto o preço médio por item passou de R$ 116,55 para R$ 117,35. Isso descreve a composição observada; não demonstra reajuste de preço do mesmo produto.

### Contribuição gerencial e apresentação

A gestão comercial pode começar a investigação pelas três categorias, examinando os produtos que compõem a diferença. Estoque, disponibilidade e campanhas são hipóteses a verificar com informações adicionais, não causas demonstradas nesta base.

O gráfico de contribuições preserva reduções, aumentos e saldo das demais categorias. As tabelas de apoio permitem reconciliar a soma das diferenças com a queda nacional. Pedidos com itens de categorias diferentes podem aparecer em várias categorias; suas contagens não são aditivas entre categorias.

### Rastreabilidade

- Código: [análise de vendas](../analises/vendas.py) e [gráficos de vendas](../graficos/vendas.py).
- Evidências: [comparação novembro/dezembro](../web/tabelas/comparacao_nov_dez.csv), [contribuições completas](../web/tabelas/contribuicoes_categorias.csv) e [categorias por mês](../web/tabelas/categorias_mensais.csv).
- Contexto adicional: [fevereiro–julho entre anos](../web/tabelas/contexto_anos.csv), sem comparação de anos completos ou comprovação de sazonalidade.
