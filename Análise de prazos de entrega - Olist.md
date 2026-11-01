# Análise dos prazos de entrega — Olist

## 1. Objetivo

Investigar o cumprimento dos prazos de entrega, medir a duração dos atrasos e identificar sua distribuição por estado de destino.

A análise busca orientar prioridades de investigação para a gestão de logística, considerando tanto a proporção de entregas atrasadas quanto a quantidade de pedidos afetados.

## 2. Público e decisões apoiadas

**Público:** gestão de logística responsável pelo acompanhamento das entregas.

**Decisões apoiadas:** definir onde aprofundar a investigação de atrasos e quais grupos de pedidos merecem acompanhamento.

Os resultados podem direcionar investigações sobre etapas do processo, vendedores, transporte e definição dos prazos prometidos. Entretanto, não demonstram, isoladamente, a causa dos atrasos nem justificam contratações ou mudanças de transportadora.

## 3. Perguntas da análise

1. Qual percentual dos pedidos entregues chegou após o dia prometido?
2. Quantos dias os pedidos atrasados demoraram além do prazo?
3. Quais estados de destino apresentam maior quantidade e maior taxa de atraso?

## 4. Dados utilizados

Fonte: [Brazilian E-Commerce Public Dataset by Olist — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

Foram utilizadas duas tabelas:

| Tabela | Finalidade |
|---|---|
| `olist_orders_dataset.csv` | Identificar pedidos, status e datas |
| `olist_customers_dataset.csv` | Identificar o estado de destino dos clientes |

Principais campos:

| Campo | Significado |
|---|---|
| `order_id` | Identificador do pedido |
| `customer_id` | Chave de relacionamento com a tabela de clientes |
| `order_status` | Status registrado do pedido |
| `order_purchase_timestamp` | Data e horário da compra |
| `order_delivered_customer_date` | Data e horário da entrega real |
| `order_estimated_delivery_date` | Data estimada, utilizada como prazo prometido nesta análise |
| `customer_state` | Estado de destino do cliente |

A data de envio foi considerada relevante para investigar etapas do processo, mas não foi necessária para calcular os indicadores desta análise.

## 5. Definição de atraso

Uma entrega foi considerada atrasada quando ocorreu **depois do dia prometido**.

```text
Entrega atrasada = data real da entrega > data prometida
```

A comparação foi feita por dia, desconsiderando os horários. Uma entrega realizada no próprio dia prometido foi considerada no prazo.

Essa escolha evita classificar como atrasada uma entrega realizada durante o dia quando a previsão está registrada à meia-noite.

## 6. Investigação da qualidade dos dados

Antes dos cálculos, foram verificadas a estrutura das tabelas, as ausências, as repetições e a coerência das datas.

| Verificação | Resultado |
|---|---:|
| Quantidade de pedidos na tabela original | 99.441 |
| Quantidade de colunas na tabela de pedidos | 8 |
| Identificadores de pedido repetidos | 0 |
| Datas reais de entrega ausentes na tabela completa | 2.965 |
| Pedidos `delivered` sem data real de entrega | 8 |
| Pedidos `delivered` sem data prometida | 0 |
| Pedidos `canceled` com data real de entrega preenchida | 6 |

A ausência de uma data de entrega não foi tratada automaticamente como erro ou atraso. Ela pode estar associada ao status do pedido ou a uma inconsistência de registro.

O cruzamento entre status e preenchimento das datas mostrou que **o status `delivered`, sozinho, não garante a presença da data real**.

### Seleção dos pedidos analisados

Foram selecionados somente pedidos que atendiam simultaneamente a três condições:

1. Status igual a `delivered`.
2. Data real de entrega preenchida.
3. Data prometida preenchida.

Dos **96.478 pedidos com status `delivered`**, oito ficaram fora do cálculo por ausência da data real. A base analisada ficou com **96.470 pedidos**.

Os registros excluídos do cálculo foram preservados na base original.

### Conversão e coerência das datas

As datas estavam armazenadas como texto e foram convertidas para o tipo de data e horário do pandas.

Após a conversão, as contagens de valores ausentes permaneceram iguais. Entre os pedidos selecionados, foram encontrados:

- **0 datas de compra ausentes.**
- **0 entregas anteriores à compra.**

Essas verificações sustentam os cálculos realizados, embora não garantam a ausência de todas as possíveis inconsistências.

## 7. Indicadores e resultados

### 7.1. Taxa de atraso

Mede a proporção de entregas atrasadas entre os pedidos elegíveis.

```text
Taxa de atraso = pedidos atrasados ÷ pedidos analisados × 100
```

| Classificação | Quantidade |
|---|---:|
| No prazo | 89.936 |
| Atrasados | 6.534 |
| Total analisado | 96.470 |

**Resultado: 6,77% das entregas analisadas chegaram após o dia prometido.**

O denominador considera somente os pedidos selecionados, e não os 99.441 registros da tabela original.

### 7.2. Duração dos atrasos

Para cada pedido atrasado:

```text
Dias de atraso = dia da entrega real − dia prometido
```

As medidas de duração consideram **somente os pedidos atrasados**. Incluir entregas antecipadas reduziria a média e responderia a outra pergunta.

| Indicador | Resultado |
|---|---:|
| Média | 10,62 dias |
| Mediana | 7 dias |
| Maior atraso registrado | 188 dias |

A mediana indica que pelo menos metade dos pedidos atrasados teve atraso de até sete dias.

A média superior à mediana sugere influência de atrasos mais longos. Isso motivou a investigação de grupos acima de determinados limites, como 100 dias. Entretanto, a diferença entre média e mediana, sozinha, não quantifica a influência desse grupo nem justifica excluir registros.

### 7.3. Quantidade e taxa de atraso por estado

Os pedidos foram relacionados à tabela de clientes por `customer_id`.

As verificações da tabela de clientes e da junção apontaram:

- **0 identificadores de cliente ausentes.**
- **0 identificadores `customer_id` repetidos na tabela de clientes.**
- **0 estados ausentes na tabela de clientes.**
- **0 pedidos sem estado após a junção.**
- **Preservação da quantidade de pedidos analisados.**
- **Reconciliação dos totais estaduais com os totais da análise.**

Para cada estado:

```text
Taxa estadual = pedidos atrasados do estado
                ÷ entregas analisadas do estado × 100
```

Destaques:

| Estado de destino | Entregas analisadas | Pedidos atrasados | Taxa de atraso |
|---|---:|---:|---:|
| Alagoas | 397 | 85 | 21,41% |
| Rio de Janeiro | 12.350 | 1.495 | 12,11% |
| São Paulo | 40.494 | 1.820 | 4,49% |

**Alagoas apresentou a maior taxa de atraso. São Paulo apresentou a maior quantidade de pedidos atrasados.** O Rio de Janeiro combinou volume elevado com taxa superior à geral de 6,77%.

O estado representa o destino do pedido, sem atribuição de responsabilidade pelo atraso.

## 8. Storytelling dos resultados

### O problema

Entre as 96.470 entregas analisadas, 6.534 chegaram após o dia prometido. A taxa de atraso foi de 6,77%.

### O impacto na espera

Nos pedidos afetados, o atraso médio foi de 10,62 dias, com mediana de sete dias. Portanto, medir apenas a frequência não descreve toda a experiência: também precisamos acompanhar a duração dos atrasos.

### A diferença entre taxa e volume

Alagoas apresentou a maior proporção de atrasos, mas São Paulo concentrou a maior quantidade de pedidos atrasados.

Essa diferença mostra que escolher o estado com a maior taxa não garante a maior redução na quantidade total de atrasos.

Em um cenário ilustrativo, eliminar todos os 85 atrasos de Alagoas evitaria menos casos do que reduzir em 10% os atrasos do Rio de Janeiro, aproximadamente 150 pedidos. A comparação demonstra escala, sem indicar qual intervenção seria mais viável.

### A orientação para a gestão

Para reduzir a quantidade de atrasos, São Paulo e Rio de Janeiro são candidatos relevantes para investigação. Alagoas merece atenção específica pela elevada proporção de entregas atrasadas.

A prioridade final deve considerar:

- Quantidade de pedidos afetados.
- Taxa de atraso.
- Duração dos atrasos.
- Causas identificadas.
- Esforço e possibilidade de melhoria.

## 9. Limitações

- A análise utiliza uma base histórica e não representa necessariamente a operação atual.
- Pedidos ainda não entregues ficaram fora deste indicador, mesmo que já estivessem atrasados.
- As comparações estaduais não controlam diferenças de período, produtos, vendedores ou rotas.
- Taxas com poucos pedidos devem ser interpretadas junto de seus volumes.
- A influência específica dos atrasos extremos sobre a média não foi quantificada neste documento.
- Os resultados descrevem padrões e orientam investigações, sem comprovar causas.
- Cenários de redução são ilustrativos e não constituem previsões.