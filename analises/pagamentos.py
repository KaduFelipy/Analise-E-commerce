from analises.vendas import pedidos

from pathlib import Path
import pandas as pd


raiz_projeto = Path(__file__).resolve().parent.parent
pasta_dados = raiz_projeto / 'dados' / 'olist'

pagamentos = pd.read_csv(pasta_dados/'olist_order_payments_dataset.csv')

# print(f'\nPrimeiros pagamentos \n{pagamentos.head().to_string(index=False)}')
# print(f'\nColunas e linhas \n{pagamentos.shape}')
# print(f'\nNome das colunas \n{pagamentos.columns.tolist()}')
# print(f'\nValores ausentes \n{pagamentos.isna().sum()}')


# print(f'\n Combinações de pedido e sequencia repetida \n{pagamentos.duplicated(subset=['order_id','payment_sequential']).sum()}')
# print(f'\nTipo das colunas \n{pagamentos.dtypes}')
# print(f'\nPagamentos com valor negativo \n{(pagamentos['payment_value'] < 0).sum()}')
# print(f'\nPagamentos com valor zerados \n{(pagamentos['payment_value'] == 0).sum()}')
# print(f'\nQuantidade de registros por forma de pagamento \n{pagamentos['payment_type'].value_counts(dropna=False)}')
# print(f'\nDistribuição da quantidade de parcelas \n{pagamentos['payment_installments'].value_counts(dropna=False).sort_index()}')

casos_para_verificar = pagamentos.loc[
    (pagamentos['payment_value'] == 0) | (pagamentos['payment_installments'] == 0) | (pagamentos['payment_type'] == 'not_defined')
].copy()

casos_para_verificar = casos_para_verificar.merge(
    pedidos[['order_id','order_status']],
    on='order_id',
    how='left',
    validate='many_to_one'
    )

# print(f'\nPagamentos investigados \n{casos_para_verificar.to_string(index=False)}')

ids_entregues = pedidos.loc[pedidos['order_status'] == 'delivered', ['order_id']].copy()

assert not ids_entregues.empty

pagamentos_entregues = pagamentos.merge(
    ids_entregues,
    on='order_id',
    how='inner',
    validate='many_to_one'
)

pedidos_sem_pagamentos = ~ ids_entregues['order_id'].isin(pagamentos_entregues['order_id'])

# print(f'\nRegistro de pagamentos de pedidos entregues \n{len(pagamentos_entregues)}')
# print(f'\nPedidos entregues com pagamento registrado \n{pagamentos_entregues['order_id'].nunique()}')
# print(f'\nPedidos entregues sem pagamento registrado \n{pedidos_sem_pagamentos.sum()}')

ids_sem_pagamentos = ids_entregues.loc[
    pedidos_sem_pagamentos,'order_id'
]

# print(f'\n Id do pedido sem pagamento \n{pedidos.loc[pedidos['order_id'].isin(ids_sem_pagamentos),['order_id','order_status','order_purchase_timestamp']].to_string(index=False)}')

resumo_formas = pagamentos_entregues.groupby('payment_type').agg(
    registros_pagamento=('order_id','size'),
    pedidos_distintos=('order_id','nunique'),
    valor_pago=('payment_value','sum')
)

assert (resumo_formas['registros_pagamento'].sum() == len(pagamentos_entregues))


total_pago = pagamentos_entregues['payment_value'].sum()

assert total_pago > 0

resumo_formas['participacao_valor'] = ( resumo_formas['valor_pago'] / total_pago * 100)
resumo_formas = resumo_formas.sort_values('valor_pago',ascending=False)

# print(f'\nFormas de pagamentos dos pedidos entregues \n{resumo_formas.round(2).to_string()}')

quantidade_pagamentos_por_pedido = (
    pagamentos_entregues.groupby('order_id')['order_id'].transform('size') #devolve a quantidade de registros do pedido em cada linha da tabela original
)

compras_cartao = pagamentos_entregues.loc[
    (quantidade_pagamentos_por_pedido == 1) 
    & (pagamentos_entregues['payment_type'] == 'credit_card')
    & (pagamentos_entregues['payment_installments'] >= 1)
    & (pagamentos_entregues['payment_value'] > 0)
].copy()

assert compras_cartao['order_id'].is_unique

# print(f'\nPedidos selecionados para comparar o parcelamento \n{len(compras_cartao)}')
# print(f'\nDistribuição dos pedidos por quantidade de parcelas \n{compras_cartao['payment_installments'].value_counts().sort_index()}')

resumo_parcelamento = compras_cartao.groupby('payment_installments').agg(
    quantidade_pedidos = ('order_id','nunique'),
    valor_medio_compra = ('payment_value','mean'),
    valor_mediano_compra = ('payment_value','median')
)

assert (resumo_parcelamento['quantidade_pedidos'].sum() == len(compras_cartao))

from analises.vendas import itens_com_categoria

resumo_parcelamento['participacao_pedidos'] = resumo_parcelamento['quantidade_pedidos'] / len(compras_cartao) * 100
parcelas_raras = resumo_parcelamento.loc[resumo_parcelamento.index > 10].copy()
categorias_pedido = itens_com_categoria.groupby('order_id')['product_category_name'].agg(['nunique', 'first'])
categorias_unicas = categorias_pedido.loc[categorias_pedido['nunique'] == 1, ['first']].rename(columns={'first': 'categoria'})
cartao_categoria = compras_cartao.merge(categorias_unicas, left_on='order_id', right_index=True, how='inner', validate='one_to_one')
excluidos_multicategoria = len(compras_cartao) - len(cartao_categoria)
resumo_categoria_parcelas = cartao_categoria.groupby(['categoria', 'payment_installments']).agg(
    pedidos=('order_id', 'size'), valor_pago=('payment_value', 'sum'),
    media=('payment_value', 'mean'), mediana=('payment_value', 'median'),
)
resumo_categoria_parcelas['participacao_pedidos_categoria'] = resumo_categoria_parcelas['pedidos'] / resumo_categoria_parcelas.groupby(level=0)['pedidos'].transform('sum') * 100
resumo_categoria_parcelas['participacao_valor_categoria'] = resumo_categoria_parcelas['valor_pago'] / resumo_categoria_parcelas.groupby(level=0)['valor_pago'].transform('sum') * 100

# print(f'\nValor da compra por quantidade de parcelas \n{resumo_parcelamento.round(2).to_string()}')
