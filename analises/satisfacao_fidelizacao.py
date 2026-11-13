from analises.avaliacoes import avaliacoes
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

pedidos_clientes = itens_vendidos[['order_id', 'customer_id']].drop_duplicates()

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