> Documento revisado em 14/11/2026. Preserva a lógica da análise inicial e incorpora os recortes implementados na versão final. Definições comuns em [Critérios dos indicadores](Crit%C3%A9rios%20dos%20indicadores.md); histórico de implementação em [Entrega da evolução](Entrega%20da%20evolu%C3%A7%C3%A3o.md).

# Análise da distribuição geográfica — Olist

## 1. Objetivo

Identificar onde se concentram os clientes e o valor vendido e em quais estados o frete representa a maior proporção do valor dos produtos.

A análise considera pedidos entregues e agrupa os resultados pelo estado de destino do cliente.

## 2. Perguntas da análise

1. Quais estados concentram mais clientes e maior valor vendido?
2. Em quais estados o frete representa a maior proporção do valor dos produtos?

## 3. Dados e critérios

Foram utilizadas as tabelas de pedidos, itens e clientes da base Olist. Os itens dos pedidos entregues vieram da análise de vendas e foram relacionados à tabela de clientes por `customer_id`.

| Indicador | Como foi calculado |
|---|---|
| Clientes distintos | Contagem de `customer_unique_id` distintos dentro de cada estado |
| Pedidos distintos | Contagem de `order_id` distintos dentro de cada estado |
| Valor vendido | Soma de `price`, sem frete |
| Frete total | Soma de `freight_value` |
| Proporção de frete | Frete total dividido pelo valor dos produtos, multiplicado por 100 |

O mesmo pedido pode aparecer em várias linhas de itens. Por isso, clientes e pedidos foram contados por identificadores distintos, enquanto os valores de produtos e frete foram somados por item.

## 4. Validações

- Nenhum valor ausente nos campos de cliente e estado utilizados.
- Nenhum `customer_id` repetido na tabela de clientes.
- Nenhum valor ausente nos campos utilizados dos itens vendidos.
- Nenhum valor de frete negativo.
- A junção preservou a quantidade de itens e todos receberam um estado de destino.

## 5. Resultados

### Concentração de clientes e vendas

Os cinco primeiros estados apareceram na mesma ordem nos rankings de clientes distintos e valor vendido.

| Estado | Clientes distintos | Pedidos | Valor dos produtos |
|---|---:|---:|---:|
| SP | 39.156 | 40.501 | R$ 5.067.633,16 |
| RJ | 11.917 | 12.350 | R$ 1.759.651,13 |
| MG | 11.001 | 11.354 | R$ 1.552.481,83 |
| RS | 5.168 | 5.345 | R$ 728.897,47 |
| PR | 4.769 | 4.923 | R$ 666.063,51 |

**São Paulo concentrou o maior número de clientes distintos e o maior valor vendido.**

### Peso do frete

| Estado | Pedidos | Frete total | Frete sobre o valor dos produtos |
|---|---:|---:|---:|
| RR | 41 | R$ 1.982,05 | 28,08% |
| MA | 717 | R$ 30.794,17 | 26,32% |
| RO | 243 | R$ 11.283,24 | 24,70% |
| AM | 145 | R$ 5.429,63 | 24,51% |
| SE | 335 | R$ 13.714,94 | 24,24% |

**Roraima teve a maior proporção de frete.** Para cada R$ 100 em produtos vendidos no estado, foram registrados R$ 28,08 em frete, considerando os 41 pedidos entregues.

## 6. Storytelling dos resultados

São Paulo lidera em clientes e valor vendido. Também registrou R$ 702.069,99 em frete, equivalentes a 13,85% do valor dos produtos. Roraima teve um total de frete bem menor, mas a maior proporção sobre o valor dos produtos, de 28,08%.

O Maranhão ajuda a interpretar essa diferença. Sua proporção, de 26,32%, ficou próxima à de Roraima e foi observada em 717 pedidos, contra 41 em Roraima.

Para a gestão, o valor vendido mostra onde as vendas se concentram. Para avaliar o peso do frete, a leitura combina **proporção, valor absoluto e quantidade de pedidos**. Esses indicadores ajudam a escolher quais estados merecem uma investigação mais detalhada.

## 7. Limitações

- A análise descreve os pedidos entregues da base histórica.
- Um cliente que comprou para estados diferentes pode ser contado em cada estado de destino. A soma das contagens estaduais pode superar o número de clientes distintos na base selecionada.
- A proporção de frete é calculada sobre os totais de cada estado. Ela não representa a média dos percentuais de cada pedido.
- A análise não verificou quanto do percentual observado se deve ao valor do frete, ao valor dos produtos ou à composição dos pedidos.

## 8. Aprofundamento: exposição comercial e logística no mesmo quadro

### Lógica de construção

O módulo `analises/geo.py` passou a reunir em `resumo_integrado` os totais comerciais por estado e os agregados de prazo de `analises/entregas.py`. A junção é feita entre resumos estaduais, com `validate='one_to_one'`, evitando replicar o atraso a cada item do pedido.

Foram acrescentados participação nas vendas, ticket e frete médio por pedido. A referência nacional usa os totais: por exemplo, proporção nacional de frete = frete total ÷ valor total dos produtos. Não é a média simples dos percentuais estaduais.

| Destino | Participação nas vendas | Taxa de atraso | Frete sobre produtos |
|---|---:|---:|---:|
| SP | 38,33% | 4,49% | 13,85% |
| RJ | 13,31% | 12,11% | 16,81% |
| MG | 11,74% | 4,57% | 17,16% |
| RS | 5,51% | 6,08% | 18,19% |
| PR | 5,04% | 4,04% | 17,36% |
| Brasil | 100,00% | 6,77% | 16,63% |

Os cinco estados são selecionados por valor dos produtos, e não por atraso ou frete. Nesse conjunto, RJ está acima da taxa nacional de atraso e da proporção nacional de frete; MG, RS e PR estão acima da proporção de frete. Isso identifica combinações para investigação, não um ranking de rentabilidade ou qualidade operacional.

### Denominadores e decisões apoiadas

Valores, ticket e frete usam **96.478 pedidos entregues**; taxa de atraso usa **96.470 avaliáveis**. Em SP são 40.501 pedidos comerciais e 40.494 avaliáveis; no RS, 5.345 e 5.344. A diferença é de elegibilidade, não uma divergência a corrigir excluindo pedidos das vendas.

Ticket e frete médio ajudam a distinguir frete absoluto elevado de uma proporção elevada por baixo valor dos produtos. Os números não separam efeitos de distância, peso, composição, contrato ou política comercial. O frete registrado não comprova o custo da empresa. A tabela de geolocalização é carregada pelo módulo, mas suas coordenadas não são usadas para gerar um mapa ou calcular distâncias na análise atual.

### Apresentação e evidências

As barras mostram participação e o gráfico de pontos compara ticket e frete nos mesmos destinos. O ranking de proporção de frete mantém quantidade de pedidos. Um mapa não foi incluído porque a pergunta atual é comparar valores exatos entre destinos.

- Código: [análise geográfica](../analises/geo.py) e [gráfico geográfico](../graficos/geo.py).
- Evidências: [quadro estadual completo](../web/tabelas/geografia.csv) e [destinos principais com referência nacional](../web/tabelas/destinos_principais.csv).
