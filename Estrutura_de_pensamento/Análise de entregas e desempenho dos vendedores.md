# Análise de entregas e desempenho dos vendedores — Olist

## 1. Objetivo

Medir o cumprimento dos prazos de entrega e identificar os vendedores associados às maiores taxas e quantidades de pedidos atrasados.

A análise busca orientar a investigação dos atrasos, considerando conjuntamente frequência, volume de pedidos afetados e quantidade de pedidos avaliados.

## 2. Público e decisões apoiadas

**Público:** gestão de logística e responsáveis pelo acompanhamento dos vendedores.

**Decisões apoiadas:** identificar grupos de pedidos e vendedores que merecem investigação mais detalhada.

A interpretação considera que um pedido pode envolver vários vendedores e que a classificação de atraso utiliza a data final de entrega do pedido.

## 3. Perguntas da análise

1. Qual percentual dos pedidos é entregue dentro do prazo prometido?
2. Quais vendedores apresentam as maiores taxas de atraso?

Durante a interpretação, acrescentamos uma pergunta complementar:

3. Quais vendedores concentram a maior quantidade de pedidos atrasados?

Essa terceira pergunta permite avaliar o volume de pedidos afetados junto das taxas.

## 4. Dados utilizados

Fonte: [Brazilian E-Commerce Public Dataset by Olist — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

Foram reutilizados resultados das análises anteriores:

| Resultado | Origem | Finalidade |
|---|---|---|
| `pedidos_analisados` | `analises/entregas.py` | Identificar pedidos com prazo avaliável e sua classificação de atraso |
| `itens_vendidos` | `analises/vendas.py` | Relacionar os pedidos entregues aos vendedores de seus itens |

Principais campos:

| Campo | Significado |
|---|---|
| `order_id` | Identificador do pedido |
| `seller_id` | Identificador do vendedor |
| `atrasados` | Classificação booleana de atraso |
| `order_delivered_customer_date` | Data real da entrega |
| `order_estimated_delivery_date` | Data estimada, utilizada como prazo prometido |

## 5. Critérios e unidade de análise

### Pedidos com prazo avaliável

Foram considerados pedidos que atendiam simultaneamente às condições:

1. Status igual a `delivered`.
2. Data real de entrega preenchida.
3. Data prometida preenchida.

A seleção contém **96.470 pedidos**.

Dos 96.478 pedidos entregues, oito ficaram fora da avaliação de prazo por ausência da data real de entrega.

### Definição de pontualidade

Uma entrega foi considerada no prazo quando ocorreu no dia prometido ou antes.

```text
Entrega no prazo = dia da entrega real ≤ dia prometido
```

Uma entrega foi considerada atrasada quando ocorreu após o dia prometido.

```text
Entrega atrasada = dia da entrega real > dia prometido
```

A comparação desconsidera os horários e utiliza os dias das duas datas.

### Unidade de análise por vendedor

Cada combinação de `order_id` e `seller_id` foi contada uma única vez.

Isso evita que um vendedor com vários itens no mesmo pedido tenha esse pedido contado repetidamente.

Exemplo:

| Pedido | Vendedor | Quantidade de itens | Relações pedido–vendedor |
|---|---|---:|---:|
| A | Vendedor 1 | 3 | 1 |
| B | Vendedor 1 | 1 | 1 |
| B | Vendedor 2 | 2 | 1 |

O pedido B aparece associado a dois vendedores. Portanto, a soma das contagens por vendedor pode superar a quantidade de pedidos distintos.

## 6. Preparação e validação dos dados

### Identificação dos vendedores

Não foram encontrados identificadores de vendedor ausentes nos itens vendidos.

Após selecionar `order_id` e `seller_id` e remover combinações repetidas, foram obtidos:

| Verificação | Resultado |
|---|---:|
| Relações entre pedidos entregues e vendedores | 97.819 |
| Pedidos distintos nessas relações | 96.478 |

A quantidade maior de relações confirma a existência de pedidos com vários vendedores.

### Associação à classificação de atraso

As relações pedido–vendedor foram conectadas aos pedidos com prazo avaliável por `order_id`.

A junção utilizou:

- `how="inner"` para selecionar relações com pedidos presentes na base de prazo avaliável.
- `validate="many_to_one"` para exigir uma única classificação de atraso por pedido.

Após a junção:

| Verificação | Resultado |
|---|---:|
| Relações com prazo avaliável | 97.811 |
| Pedidos distintos com prazo avaliável | 96.470 |

Foram verificadas a preservação dos pedidos elegíveis e a ausência de classificações de atraso vazias.

### Validação do resumo por vendedor

O agrupamento por `seller_id` calculou:

- Quantidade de pedidos distintos avaliados.
- Quantidade de pedidos atrasados.
- Taxa de atraso.

Também foram verificadas:

- A reconciliação da soma de pedidos avaliados por vendedor com as 97.811 relações.
- A condição de que os pedidos atrasados de cada vendedor não superem seus pedidos avaliados.
- A ordenação decrescente do ranking por quantidade de atrasos.

## 7. Indicadores e resultados

### 7.1. Taxa geral de entregas no prazo

```text
Taxa de entregas no prazo (%) =
pedidos entregues no prazo ÷ pedidos analisados × 100
```

| Classificação | Quantidade |
|---|---:|
| Pedidos analisados | 96.470 |
| Entregues no prazo | 89.936 |
| Atrasados | 6.534 |

**Resultado: 93,23% dos pedidos analisados foram entregues no prazo.**

A taxa geral de atraso foi de **6,77%** e serviu como referência para a leitura dos resultados dos vendedores.

### 7.2. Taxa de atraso por vendedor

```text
Taxa de atraso do vendedor (%) =
pedidos atrasados associados ao vendedor
÷ pedidos avaliados associados ao vendedor × 100
```

O ranking foi ordenado primeiro pela taxa de atraso e, nos empates, pela quantidade de pedidos avaliados.

Os dez primeiros vendedores apresentaram **100% de atraso**:

- Cinco vendedores tinham dois pedidos avaliados, ambos atrasados.
- Cinco vendedores tinham um pedido avaliado, que estava atrasado.

Essas taxas exigem leitura conjunta com seus pequenos volumes. Poucos pedidos adicionais podem alterar bastante os percentuais.

### 7.3. Quantidade de pedidos atrasados por vendedor

Para complementar a análise, os vendedores foram ordenados pela quantidade de pedidos atrasados. A taxa foi utilizada como critério de desempate.

| Vendedor | Pedidos avaliados | Pedidos atrasados | Taxa de atraso |
|---|---:|---:|---:|
| `4a3ca9315b744ce9f8e9374361493884` | 1.772 | 172 | 9,71% |
| `1f50f920176fa81dab994f9023523100` | 1.399 | 124 | 8,86% |
| `4869f7a5dfa277a7dca6462dcf3b52b2` | 1.124 | 118 | 10,50% |
| `ea8482cd71df3c1969d7b9473ff13abc` | 1.132 | 96 | 8,48% |
| `6560211a19b47992c3666cc44a7e94c0` | 1.819 | 96 | 5,28% |
| `7c67e1448b00f6e969d365cea6b010ab` | 973 | 89 | 9,15% |
| `da8622b14eb17ae2831f4ac5b9dab84a` | 1.311 | 87 | 6,64% |
| `cc419e0650a3c5ba77189a1882b7556a` | 1.651 | 87 | 5,27% |
| `8b321bb669392f5163d04c59e235e066` | 930 | 81 | 8,71% |
| `955fee9216a65b617aa5c0531780ce60` | 1.261 | 77 | 6,11% |

Destaques:

- O maior volume foi de **172 atrasos em 1.772 pedidos**, com taxa de **9,71%**.
- Entre os dez vendedores desse ranking, a maior taxa foi de **10,50%**, correspondente a **118 atrasos em 1.124 pedidos**.
- Um vendedor com **96 atrasos em 1.819 pedidos** apareceu pelo volume, embora sua taxa de **5,28%** estivesse abaixo da referência geral.

## 8. Storytelling dos resultados

### A pontualidade geral

Dos 96.470 pedidos com prazo avaliável, 89.936 chegaram no dia prometido ou antes. A taxa de pontualidade foi de **93,23%**.

Os 6.534 atrasos restantes motivaram a investigação dos pedidos associados aos vendedores.

### As maiores taxas exigem contexto

O ranking por taxa apresentou vendedores com 100% de atraso. Entretanto, cada um dos dez primeiros possuía somente um ou dois pedidos avaliados.

O percentual descreve esses pedidos, mas o volume reduzido exige cuidado para avaliar a recorrência do problema.

### A quantidade revela o alcance do problema

Ao ordenar pela quantidade de atrasos, surgiram vendedores associados a dezenas ou centenas de pedidos afetados.

O primeiro apresentou **172 atrasos em 1.772 pedidos**, com taxa de **9,71%**, acima da referência geral de 6,77%.

Esse caso combina volume e frequência que merecem investigação.

### A prioridade depende de taxa e volume

Dois vendedores apresentaram 96 pedidos atrasados cada. Um tinha taxa de 8,48% e o outro, 5,28%, pois seus volumes avaliados eram diferentes.

A mesma quantidade de atrasos pode representar frequências distintas. Da mesma forma, taxas iguais podem envolver quantidades muito diferentes de pedidos.

A leitura conjunta dos indicadores ajuda a selecionar grupos para investigação.

### A orientação para a gestão

Os vendedores associados a muitos atrasos são candidatos para aprofundar a análise dos pedidos. As taxas ajudam a contextualizar a frequência do problema em relação ao volume atendido.

A classificação disponível utiliza a entrega final do pedido. A investigação precisa examinar as etapas do processo antes de atribuir responsabilidade ou escolher uma intervenção.

## 9. Apresentação dos resultados

O gráfico apresenta os dez vendedores com maior quantidade de pedidos atrasados em dois painéis alinhados:

1. Quantidade de pedidos atrasados.
2. Taxa de atraso, acompanhada do número de pedidos avaliados.

A taxa geral de atraso de 6,77% aparece como referência.

O título apresenta a pontualidade geral de 93,23%. A página HTML acrescenta a interpretação dos resultados, os critérios de contagem e as limitações.

## 10. Limitações

- A análise descreve uma base histórica e não representa necessariamente o desempenho atual dos vendedores.
- Foram considerados somente pedidos entregues com as duas datas necessárias preenchidas.
- Pedidos ainda não entregues ficaram fora da avaliação, mesmo que já tivessem ultrapassado o prazo.
- Um pedido com vários vendedores aparece associado a cada um deles. A soma dos atrasos por vendedor pode contar o mesmo pedido mais de uma vez.
- A classificação de atraso usa a entrega final do pedido e não identifica qual vendedor ou etapa causou o atraso.
- A referência geral de 6,77% considera pedidos distintos. Os indicadores dos vendedores utilizam as associações de cada vendedor com esses pedidos.
- Não foram controladas diferenças de período, destinos, produtos ou etapas logísticas entre vendedores.
- Taxas baseadas em poucos pedidos são sensíveis a pequenas mudanças nas contagens.
- A análise orienta a investigação e não comprova causas ou responsabilidade individual.