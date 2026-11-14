# Análise de pagamentos e parcelamento — Olist

Documento revisado em 14/11/2026. Definições gerais: [Critérios dos indicadores](Crit%C3%A9rios%20dos%20indicadores.md).

## 1. Objetivo e decisões apoiadas

Descrever como os pedidos entregues foram pagos e como parcelas se relacionam com valor e categoria. A gestão comercial pode identificar combinações relevantes para investigação; a análise não estima o efeito de oferecer mais parcelas sobre vendas, margem ou conversão.

## 2. Perguntas

1. Quais formas concentram o valor pago registrado?
2. Como média, mediana e quantidade de pedidos variam entre parcelamentos?
3. Em quais categorias oito ou dez parcelas apresentam volume e valor relevantes?

## 3. Dados e unidade de análise

O módulo `analises/pagamentos.py` lê `olist_order_payments_dataset.csv` e usa pedidos de `analises/vendas.py`. Para categorias, utiliza `itens_com_categoria`, que relaciona pedidos entregues, itens e produtos.

Cada linha da tabela de pagamentos é um **registro de pagamento**, não necessariamente um pedido completo. Um pedido pode ter vários registros e formas. A chave composta `order_id`/`payment_sequential` não apresentou duplicação na conferência da base local; o vínculo aos pedidos usa `many_to_one`.

## 4. Caminho dos cálculos

### Distribuição das formas

Selecionar os IDs de pedidos `delivered`, relacionar os registros de pagamento e agrupar por `payment_type`. Contar registros e pedidos distintos separadamente; somar `payment_value` e dividir pelo total pago registrado.

Foram encontrados **100.756 registros para 96.477 pedidos entregues**; um dos 96.478 pedidos entregues não tinha registro correspondente. O total pago associado foi **R$ 15.422.461,77**. Contagens de pedidos entre formas não devem ser somadas como grupos exclusivos.

| Forma | Pedidos que utilizaram | Participação no valor pago |
|---|---:|---:|
| Cartão de crédito | 74.304 | 78,46% |
| Boleto | 19.191 | 17,96% |
| Voucher | 3.679 | 2,22% |
| Cartão de débito | 1.485 | 1,35% |

### Comparação por parcelas

Usar `groupby('order_id').transform('size')` para identificar a quantidade de registros por pedido. Selecionar pagamento único no cartão, parcelas ≥ 1 e valor positivo. Os **71.841 pedidos** selecionados são únicos; nesse recorte, o registro representa o pagamento total registrado do pedido, que pode incluir frete.

Agrupar por parcelas e calcular quantidade, participação no recorte, média e mediana de `payment_value`. Acima de dez parcelas existem **317 pedidos, 0,44% do recorte**. Sua baixa frequência não deve receber o mesmo peso interpretativo dos grupos numerosos.

### Complemento por categoria

Contar categorias distintas de cada pedido, preservando “Sem categoria”. Relacionar somente pedidos de uma categoria ao recorte de cartão, com `one_to_one`. São **71.253 pedidos**, com **588 multicategoria excluídos**. O pagamento integral entra uma vez; não há rateio arbitrário nem multiplicação por item.

```text
Participação nos pedidos da categoria = pedidos do grupo ÷ pedidos da categoria no complemento × 100
Participação no valor da categoria = pagamento do grupo ÷ pagamento da categoria no complemento × 100
```

## 5. Descoberta e uso gerencial

Entre oito e dez parcelas, o grupo com maior valor pago no complemento é **relógios e presentes em oito parcelas**: 687 pedidos e R$ 298.535,90. Representa **16,01% dos pedidos e 29,04% do valor pago da categoria** naquele complemento. A média é R$ 434,55 e a mediana R$ 273,47.

O resultado identifica uma concentração comercial. O passo seguinte é investigar os produtos e a composição desse grupo antes de avaliar uma mudança nas condições de pagamento. Maior valor médio não demonstra que o parcelamento fez o cliente gastar mais.

## 6. Validações e limites

- A soma de registros por forma reconcilia com os pagamentos selecionados.
- O recorte de cartão tem `order_id` único e suas contagens por parcelas reconciliam com o total.
- O complemento mais as exclusões multicategoria reconcilia com os 71.841 pedidos.
- As participações têm denominadores diferentes: total pago por forma, recorte de cartão ou categoria no complemento.
- Valores pagos podem incluir frete e não representam necessariamente apenas produtos, lucro ou receita da plataforma.
- Pedidos cancelados, pagamentos múltiplos e multicategoria não fazem parte de todos os recortes. Grupos pequenos e composição de produtos limitam comparações.
- Não há dados suficientes para medir taxas financeiras, antecipação, inadimplência ou rentabilidade das parcelas.

## 7. Gráfico, HTML e evidências

O gráfico usa barras para participação das formas, pontos para média/mediana e volume alinhado por parcelas. A figura principal mostra uma a dez parcelas; os demais grupos permanecem no CSV. O HTML destaca a seleção comercial por categoria, explicando a cobertura.

- Código: [pagamentos](../analises/pagamentos.py) e [gráfico](../graficos/pagamentos.py).
- Evidências: [formas](../web/tabelas/formas_pagamento.csv), [todas as parcelas](../web/tabelas/parcelamento.csv), [categorias/parcelas](../web/tabelas/categoria_parcelas.csv) e [grupo principal](../web/tabelas/parcelamento_principal.csv).
