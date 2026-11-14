import pandas as pd
from analises.avaliacoes import avaliacoes, classificar_momento
from analises.entregas import pedidos_analisados
from analises.clientes import clientes
from analises.vendas import itens_vendidos

avaliacoes_por_pedido = avaliacoes['order_id'].value_counts()

# print(f'\n Pedidos destintos: {avaliacoes['order_id'].nunique()}')
# print(f'\n Pedidos com mais de uma avaliacao: {(avaliacoes_por_pedido>1).sum()}')
# print(f'\n Linhas repetidas: {avaliacoes.duplicated().sum()}')

avaliacoes_por_pedido = avaliacoes.groupby('order_id').agg(
    nota_media = ('review_score', 'mean'),
    quantidade_avaliacoes = ('review_score', 'size')
)

assert avaliacoes_por_pedido.index.is_unique
assert avaliacoes_por_pedido['nota_media'].between(1,5).all()

# print(f'\n Avaliacoes consolidadas por pedido: {avaliacoes_por_pedido.head().to_string()}')

pedidos_avaliados = pedidos_analisados[['order_id','atrasados']].merge(
    avaliacoes_por_pedido,
    left_on='order_id', #left_on='order_id' usa a coluna de pedidos como chave.
    right_index=True, #right_index=True usa o índice da tabela de avaliações, onde order_id ficou após o agrupamento.
    how='left', #preserva todos os pedidos com prazo avaliável
    validate='one_to_one' #exige uma linha por pedido em cada lado.
)

assert len(pedidos_avaliados) == len(pedidos_analisados)

# print(f'\nPedidos com avaliação \n{len(pedidos_avaliados)}')
# print(f'\nPedidos sem avaliação \n{pedidos_avaliados['nota_media'].isna().sum()}')

resumo_satisfacao = pedidos_avaliados.groupby('atrasados').agg(
    total_pedidos = ('order_id', 'size'),
    pedidos_com_nota = ('nota_media','count'),
    nota_media = ('nota_media','mean'),
    nota_mediana = ('nota_media', 'median')
)

resumo_satisfacao['cobertura_avaliacoes'] = (
    resumo_satisfacao['pedidos_com_nota'] / resumo_satisfacao['total_pedidos'] * 100
)

assert resumo_satisfacao['total_pedidos'].sum() == len(pedidos_avaliados)

# print(f'\n Avaliacoes por situacao de entrega \n{resumo_satisfacao.round(2).to_string()}') #False é as entregas atrasadas, e True as entregas no prazo

pedidos_clientes = itens_vendidos[['order_id', 'customer_id', 'order_purchase_timestamp']].drop_duplicates()

pedidos_clientes = pedidos_clientes.merge(
    clientes[['customer_id', 'customer_unique_id']],
    on='customer_id',
    how='left',
    validate='many_to_one',
)

assert pedidos_clientes['order_id'].is_unique
assert pedidos_clientes['customer_unique_id'].notna().all()
assert len(pedidos_clientes) == itens_vendidos['order_id'].nunique()

pedidos_por_cliente = pedidos_clientes.groupby('customer_unique_id').agg(
    quantidade_pedidos=('order_id', 'nunique'),
)

pedidos_por_cliente['recorrente'] = (pedidos_por_cliente['quantidade_pedidos'] >= 2)


def calcular_recompra(pedidos, corte):
    assert pedidos['order_id'].is_unique
    dias = pedidos.assign(dia=pedidos['order_purchase_timestamp'].dt.normalize())
    dias = dias[['customer_unique_id', 'dia']].drop_duplicates().sort_values('dia')
    dias['ordem_dia'] = dias.groupby('customer_unique_id').cumcount()
    primeira = dias.groupby('customer_unique_id')['dia'].min().rename('primeira_compra')
    posterior = dias.loc[dias['ordem_dia'] == 1].set_index('customer_unique_id')['dia'].rename('primeira_posterior')
    r = primeira.to_frame().join(posterior)
    r['dias_ate_recompra'] = (r['primeira_posterior'] - r['primeira_compra']).dt.days
    r['outro_dia'] = r['primeira_posterior'].notna()
    r['elegivel_90d'] = (pd.Timestamp(corte).normalize() - r['primeira_compra']).dt.days >= 90
    r['recompra_90d'] = r['elegivel_90d'] & r['dias_ate_recompra'].between(1, 90)
    return r


data_corte_recompra = pedidos_clientes['order_purchase_timestamp'].max().normalize()
recompra_clientes = calcular_recompra(pedidos_clientes, data_corte_recompra)
resumo_recompra = pd.Series({
    'clientes': len(recompra_clientes),
    'multiplos_pedidos': int(pedidos_por_cliente['recorrente'].sum()),
    'outro_dia': int(recompra_clientes['outro_dia'].sum()),
    'elegiveis_90d': int(recompra_clientes['elegivel_90d'].sum()),
    'recompraram_90d': int(recompra_clientes['recompra_90d'].sum()),
})
resumo_recompra['taxa_90d'] = resumo_recompra['recompraram_90d'] / resumo_recompra['elegiveis_90d'] * 100

registros_avaliados = classificar_momento(avaliacoes.merge(
    pedidos_analisados[['order_id', 'atrasados', 'dias_apos_prazo', 'order_delivered_customer_date', 'order_estimated_delivery_date']],
    on='order_id', how='inner', validate='many_to_one',
))
registros_avaliados['recorte_resposta'] = registros_avaliados['momento_resposta']
antes = registros_avaliados['momento_resposta'].eq('Antes da entrega')
registros_avaliados.loc[antes & ~registros_avaliados['espera_apos_prazo'], 'recorte_resposta'] = 'Antes da entrega, até o dia prometido'
registros_avaliados.loc[antes & registros_avaliados['espera_apos_prazo'], 'recorte_resposta'] = 'Antes da entrega, após o dia prometido'
notas_por_recorte = registros_avaliados.groupby(['order_id', 'atrasados', 'recorte_resposta']).agg(
    nota_media=('review_score', 'mean'), registros=('review_score', 'size'),
).reset_index()
resumo_momento = notas_por_recorte.groupby(['atrasados', 'recorte_resposta']).agg(
    pedidos=('order_id', 'nunique'), registros=('registros', 'sum'), nota_media=('nota_media', 'mean'),
)
resumo_momento['cobertura_situacao'] = resumo_momento['pedidos'] / resumo_momento.index.get_level_values('atrasados').map(pedidos_analisados.groupby('atrasados').size()) * 100
assert resumo_momento['registros'].sum() == len(registros_avaliados)
pedidos_multiplas_avaliacoes = int((avaliacoes.groupby('order_id').size() > 1).sum())
pedidos_multiplos_recortes = int((notas_por_recorte.groupby('order_id').size() > 1).sum())
percentual_respostas_antes_atrasados = registros_avaliados.loc[registros_avaliados['atrasados'], 'momento_resposta'].eq('Antes da entrega').mean() * 100

registros_avaliados['faixa_atraso'] = pd.cut(registros_avaliados['dias_apos_prazo'], [0, 7, 15, 30, float('inf')], labels=['1–7', '8–15', '16–30', 'Acima de 30'])
notas_faixas = registros_avaliados.loc[registros_avaliados['atrasados']].groupby(
    ['order_id', 'faixa_atraso', 'recorte_resposta'], observed=True,
).agg(nota_media=('review_score', 'mean'), registros=('review_score', 'size')).reset_index()
resumo_notas_faixas = notas_faixas.groupby(['faixa_atraso', 'recorte_resposta'], observed=True).agg(
    pedidos=('order_id', 'nunique'), registros=('registros', 'sum'), nota_media=('nota_media', 'mean'),
)

# print(f'\nClientes por classificação de recorrência \n{pedidos_por_cliente['recorrente'].value_counts()}') #False é os cliente socm pedidos entregues e True com pedidos recorrentes.
# print(f'\nTotal de clientes distintos \n{len(pedidos_por_cliente)}')




itens_com_recorrencia = itens_vendidos.merge(
    pedidos_clientes[['order_id', 'customer_unique_id']],
    on='order_id',
    how='left',
    validate='many_to_one',
)

itens_com_recorrencia = itens_com_recorrencia.merge(
    pedidos_por_cliente[['recorrente']],
    left_on='customer_unique_id',
    right_index=True,
    how='left',
    validate='many_to_one',
)

assert len(itens_com_recorrencia) == len(itens_vendidos)
assert itens_com_recorrencia['recorrente'].notna().all()




resumo_recorrencia = itens_com_recorrencia.groupby('recorrente').agg(
    clientes_distintos=('customer_unique_id', 'nunique'),
    pedidos_distintos=('order_id', 'nunique'),
    valor_produtos=('price', 'sum'),
)

assert resumo_recorrencia['clientes_distintos'].sum() == len(pedidos_por_cliente)
assert resumo_recorrencia['pedidos_distintos'].sum() == len(pedidos_clientes)

resumo_recorrencia['participacao_clientes'] = (resumo_recorrencia['clientes_distintos'] / resumo_recorrencia['clientes_distintos'].sum() * 100)
resumo_recorrencia['participacao_valor'] = (resumo_recorrencia['valor_produtos'] / itens_vendidos['price'].sum() * 100)

# print(f'\nParticipação dos clientes recorrentes \n{resumo_recorrencia.round(2).to_string()}') #False sem recorrencia, True com recorrencia


assert resumo_recorrencia['pedidos_distintos'].gt(0).all()
assert resumo_recorrencia['clientes_distintos'].gt(0).all()

resumo_recorrencia['ticket_medio'] = (resumo_recorrencia['valor_produtos'] / resumo_recorrencia['pedidos_distintos'])

resumo_recorrencia['valor_por_cliente'] = (resumo_recorrencia['valor_produtos'] / resumo_recorrencia['clientes_distintos'])

# print('\nValor médio por pedido e por cliente:')
# print(
#     resumo_recorrencia[
#         ['clientes_distintos', 'pedidos_distintos',
#          'ticket_medio', 'valor_por_cliente']
#     ].round(2).to_string()
# ) 
