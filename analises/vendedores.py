from analises.entregas import pedidos_analisados
from analises.vendas import itens_vendidos

assert len(pedidos_analisados) > 0
assert pedidos_analisados['atrasados'].notna().all()

total_pedidos = len(pedidos_analisados)
quantidade_no_prazo = (~pedidos_analisados['atrasados']).sum()

taxa_no_prazo = quantidade_no_prazo / total_pedidos * 100

# print(f'\nPedidos analisados: {total_pedidos}')
# print(f'\nPedidos entregues no prazo: {quantidade_no_prazo}')
# print(f'\nTaxa de entregas no prazo: {taxa_no_prazo:.2f}')

pedidos_vendedores = itens_vendidos[['order_id','seller_id']].drop_duplicates()

# print(f'\nVendedores ausentes \n{itens_vendidos['seller_id'].isna().sum()}')
# print(f'\nRelação pedidos / vendedores: {len(pedidos_vendedores)}')
# print(f'Quantidade de pedidos distintos: {pedidos_vendedores['order_id'].nunique()}')

assert pedidos_analisados['order_id'].isin(
    pedidos_vendedores['order_id']
).all()

entregas_vendedores = pedidos_vendedores.merge(
    pedidos_analisados[['order_id','atrasados']],
    on='order_id',
    how='inner',
    validate='many_to_one',
)

assert entregas_vendedores['order_id'].nunique()== len(pedidos_analisados)
assert entregas_vendedores['atrasados'].notna().all()

# print(f'\nRelações entre pedidos e vendedores com prazo avaliável: {len(entregas_vendedores)}')
# print(f'\nPedidos distintos com prazo avaliável: {entregas_vendedores['order_id'].nunique()}')

resumo_vendedores = entregas_vendedores.groupby('seller_id').agg(
    pedidos_avaliados = ('order_id','nunique'),
    pedidos_atrasados = ('atrasados','sum')
)

resumo_vendedores['taxa_atraso'] = (
    resumo_vendedores['pedidos_atrasados'] / resumo_vendedores['pedidos_avaliados'] * 100
)

assert resumo_vendedores['pedidos_avaliados'].sum() == len(entregas_vendedores)
assert resumo_vendedores['pedidos_atrasados'].le(
    resumo_vendedores['pedidos_avaliados']
).all()

ranking_vendedores = resumo_vendedores.sort_values(
    ['taxa_atraso', 'pedidos_avaliados'],
    ascending=[False,False]
)

# print(f'\nDez vendedores com maior taxa de atraso: {ranking_vendedores.head(10).round(2).to_string()}')

ranking_quantidade = resumo_vendedores.sort_values(
    ['pedidos_atrasados','taxa_atraso'],
    ascending=[False,False]
)

# print(f'\nDez vendedores com maior quantidade de pedidos atrasados: {ranking_quantidade.head(10).round(2).to_string()}')