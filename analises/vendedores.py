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

from analises.entregas import pedidos_por_estado

rotulos_vendedores = {vendedor: f'Vendedor {i + 1}' for i, vendedor in enumerate(sorted(resumo_vendedores.index))}
resumo_vendedores['rotulo'] = resumo_vendedores.index.map(rotulos_vendedores)
quantidade_vendedores = pedidos_vendedores.groupby('order_id')['seller_id'].nunique()
ids_unicos = quantidade_vendedores.loc[quantidade_vendedores == 1].index
entregas_vendedor_unico = pedidos_vendedores.loc[pedidos_vendedores['order_id'].isin(ids_unicos)].merge(
    pedidos_por_estado[['order_id', 'customer_state', 'mes_compra', 'atrasados']],
    on='order_id', how='inner', validate='one_to_one',
)
pedidos_excluidos_multivendedor = len(pedidos_analisados) - len(entregas_vendedor_unico)
comparacao_celulas = entregas_vendedor_unico.groupby(['seller_id', 'customer_state', 'mes_compra']).agg(
    pedidos_avaliaveis=('order_id', 'size'), atrasados=('atrasados', 'sum'),
)
comparacao_celulas['taxa_atraso'] = comparacao_celulas['atrasados'] / comparacao_celulas['pedidos_avaliaveis'] * 100
comparacao_celulas['rotulo'] = comparacao_celulas.index.get_level_values('seller_id').map(rotulos_vendedores)
referencia_celulas = entregas_vendedor_unico.groupby(['customer_state', 'mes_compra']).agg(
    pedidos_referencia=('order_id', 'size'), atrasados_referencia=('atrasados', 'sum'),
)
referencia_celulas['taxa_referencia'] = referencia_celulas['atrasados_referencia'] / referencia_celulas['pedidos_referencia'] * 100
comparacao_celulas = comparacao_celulas.join(referencia_celulas, on=['customer_state', 'mes_compra'], validate='many_to_one')

trimestrais = entregas_vendedor_unico.loc[entregas_vendedor_unico['mes_compra'].between('2017-04', '2018-06')].copy()
trimestrais['trimestre_compra'] = trimestrais['mes_compra'].dt.asfreq('Q')
comparacao_trimestral = trimestrais.groupby(['seller_id', 'customer_state', 'trimestre_compra']).agg(pedidos_avaliaveis=('order_id', 'size'), atrasados=('atrasados', 'sum'))
celulas_trimestre = trimestrais.groupby(['customer_state', 'trimestre_compra']).agg(total=('order_id', 'size'), atrasos_total=('atrasados', 'sum'))
comparacao_trimestral = comparacao_trimestral.join(celulas_trimestre, on=['customer_state', 'trimestre_compra'], validate='many_to_one')
comparacao_trimestral['pedidos_outros_vendedores'] = comparacao_trimestral['total'] - comparacao_trimestral['pedidos_avaliaveis']
comparacao_trimestral['atrasados_outros_vendedores'] = comparacao_trimestral['atrasos_total'] - comparacao_trimestral['atrasados']
comparacao_trimestral['taxa_atraso'] = comparacao_trimestral['atrasados'] / comparacao_trimestral['pedidos_avaliaveis'] * 100
comparacao_trimestral['taxa_outros_vendedores'] = comparacao_trimestral['atrasados_outros_vendedores'] / comparacao_trimestral['pedidos_outros_vendedores'].replace(0, float('nan')) * 100
ranking_trimestral = trimestrais.groupby('seller_id').agg(atrasados=('atrasados', 'sum'), pedidos_avaliaveis=('order_id', 'size')).reset_index().sort_values(['atrasados', 'pedidos_avaliaveis', 'seller_id'], ascending=[False, False, True]).head(10)
comparacao_trimestral['rotulo'] = comparacao_trimestral.index.get_level_values('seller_id').map(rotulos_vendedores)
comparacao_trimestral_selecionada = comparacao_trimestral.loc[comparacao_trimestral.index.get_level_values('seller_id').isin(ranking_trimestral['seller_id'])]

# print(f'\nDez vendedores com maior quantidade de pedidos atrasados: {ranking_quantidade.head(10).round(2).to_string()}')
