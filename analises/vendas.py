import pandas as pd
from pathlib import Path
from analises.produtos import produtos
from math import isclose


raiz_projeto = Path(__file__).resolve().parent.parent

pasta_dados=(
    raiz_projeto
    /'dados'
    /'olist'
)

pedidos = pd.read_csv(pasta_dados/'olist_orders_dataset.csv')
itens = pd.read_csv(pasta_dados/'olist_order_items_dataset.csv')


# print(itens.head().to_string(index=False))
# print(itens.shape)
# print(itens.columns.tolist())

# print(f'\nPedidos ausentes: \n{pedidos[['order_id','order_status','order_purchase_timestamp']].isna().sum()}')
# print(f'\nPedidos repetidos: \n{pedidos['order_id'].duplicated().sum()}')
# print(f'\nItens ausentes: \n{itens[['order_id','order_item_id','product_id','price']].isna().sum()}')
# print(f'\nRelação de repetidos: pedidos/itens \n{itens.duplicated(subset=['order_id','order_item_id']).sum()}')# Primeira vez que apresento o subset. Ele seleciona somente as colunas que serão consideradas nesse caso pra verificar a duplicidade.
# print(f'\nTipo de dado da col preço: \n{itens['price'].dtype}')

# print(f'\nPreços \n{itens['price'].describe()}') #Primeira vez que aparece o describe também. Ele gera um resumo rápido da quantidade, média, desvio padrão, mínimo, quartis e máximo.
# print(f'\nItens invalidos \n{(itens['price']<=0).sum()}')


pedidos_entregues = pedidos.loc[
    pedidos['order_status'] == 'delivered'
].copy()

# print(f'\nPedidos entregues \n{len(pedidos_entregues)}')

# sem_itens = ~pedidos_entregues['order_id'].isin(itens['order_id']) # '~' é usado para inverter o resultado, parecido com um if not.
# print(f'Pedidos entregues sem itens \n{sem_itens.sum()}')

itens_vendidos = itens.merge(
    pedidos_entregues[['order_id', 'customer_id','order_purchase_timestamp']],
    on='order_id',
    how='inner', #mantém somente itens que correspondem aos pedidos entregues selecionados.
    validate='many_to_one' #permite vários itens por pedido, exigindo um único registro correspondente na tabela de pedidos.
)

assert itens_vendidos['order_id'].nunique() == len(pedidos_entregues) #nunique: conta identificadores distintos, evitando contar um pedido várias vezes.

# print(f'\nItens vendidos: \n{len(itens_vendidos)}')
# print(f'\nProdutos distintos \n{itens_vendidos['order_id'].nunique()}')
# print(f'\nValor total dos produtos \n{itens_vendidos['price'].sum():.2f}')

itens_vendidos['order_purchase_timestamp'] = pd.to_datetime(
    itens_vendidos['order_purchase_timestamp'],
    format='%Y-%m-%d %H:%M:%S',
    errors='raise'
)

itens_vendidos['mes_compra']=(
    itens_vendidos['order_purchase_timestamp'].dt.to_period('M') #dt.to_period('M'): Ele transforma as datas yyyy-mm-dd hh:mm:ss em yyyy-mm. Assim podemos compara os valores por ano e mês.
)

vendas_mensais = itens_vendidos.groupby('mes_compra').agg(
    valor_vendido=('price', 'sum'),
    quantidade_pedidos=('order_id','nunique')
)

assert vendas_mensais['quantidade_pedidos'].sum() == len(pedidos_entregues)

# print(f'\nVendas por mês \n{vendas_mensais.round(2).to_string()}')

cobertura_mensal = itens_vendidos.groupby('mes_compra').agg(
    primeira_compra=('order_purchase_timestamp', 'min'),
    ultima_compra = ('order_purchase_timestamp', 'max')
)

# print(f'\nIntervalo de compra por mês \n{cobertura_mensal.to_string()}')

vendas_comparaveis = vendas_mensais.loc[
    '2017-02':'2018-07' #define a localização de:até
].copy() 

vendas_comparaveis['variacao_percentual'] = (
    vendas_comparaveis['valor_vendido'].pct_change(fill_method=None)*100 #pct_change: calcula a variação relativa entre as linhas anteriores. exemplo: valor atual / valor anterior - 1. o fill_method=None é para não preencher valores ausentes automáticamente, nesse caso o mês 02-2017 seria a base primária mas como não tem mês anterior a porcentagem começa pelo mês 03-2017
)

# print(f'\nEvolução  Mensal das vendas \n{vendas_comparaveis.round(2).to_string()}')

variacao = vendas_comparaveis['variacao_percentual'].dropna() #dropna: retira os resultados ausentes dessa seleção, como a variação do primeiro mês.

mes_maior_alta = variacao.idxmax() #idxmax: devolve o mês associado ao maior valor.
mes_maior_queda = variacao.idxmin() #idxmin: devolve o mês associado ao menor valor.

# print('\nMaior variação mensal\n')
# print(vendas_comparaveis.loc[mes_maior_alta, ['valor_vendido', 'quantidade_pedidos','variacao_percentual']])
# print('\nMenor variação mensal\n')
# print(vendas_comparaveis.loc[mes_maior_queda, ['valor_vendido', 'quantidade_pedidos','variacao_percentual']])


#Comparação por ano. Se tivesse todos os meses preenchidos.
# vendas_2017 = vendas_mensais.loc['2017-01':'2017-12'].copy()
# vendas_2018 = vendas_mensais.loc['2018-01':'2018-12'].copy()

# total_2017 = vendas_2017['valor_vendido'].sum()
# total_2018 = vendas_2018['valor_vendido'].sum()

# print(f'Total de vendas em 2017: R${total_2017:.2f}')
# print(f'Total de vendas em 2018: R${total_2018:.2f}')


# #Comparação dos meses de temporada de cada ano. Se os intervalos fossem iguais
# temporada_2017 = vendas_mensais.loc['2017-09':'2017-12'].copy()
# temporada_2018 = vendas_mensais.loc['2018-09':'2018-12'].copy()

# assert temporada_2017.index.month.tolist() == list(range(9,13)) #.index.month extrai os números dos meses do índice.
# assert temporada_2018.index.month.tolist() == list(range(9,13))

# total_temporada_2017 = temporada_2017['valor_vendido'].sum()
# total_temporada_2018 = temporada_2018['valor_vendido'].sum()

# assert total_temporada_2017 > 0
# assert total_temporada_2018 > 0

# variacao_periodo = (total_temporada_2018/total_temporada_2017 - 1)*100
# print(f'Total vendido na temporada 2017: R${total_temporada_2017:.2f}')
# print(f'Total vendido na temporada 2018: R${total_temporada_2018:.2f}')
# print(f'Variação entre os períodos: {variacao_periodo:2f}%')

itens_com_categoria = itens_vendidos.merge(
    produtos[['product_id','product_category_name']],
    on='product_id',
    how='left',
    validate='many_to_one',
    indicator=True #indicator=True: ela cria uma coluna chamada _merge, mostrando se houve correspondência. Aparece both se o produto tem correspondencia, se não aparece left_only.
)

assert len(itens_com_categoria) == len(itens_vendidos)

# print(f'\nItens vendidos sem produtos correspondentes: \n{(itens_com_categoria['_merge'] == 'left_only').sum()}')
# print(f'\nItens vendidos sem categoria: \n{itens_com_categoria['product_category_name'].isna().sum()}')

itens_com_categoria['product_category_name'] = (
    itens_com_categoria['product_category_name'].fillna('Sem categoria') #fillna("Sem categoria"): substitui somente os valores ausentes por Sem categoria. Não estamos deduzindo a categoria original.
)

vendas_por_categoria = itens_com_categoria.groupby(
    'product_category_name'
).agg(
    valor_vendido = ('price', 'sum'),
    quantidade_itens = ('order_item_id','size')
)

total_vendido = itens_vendidos['price'].sum()

assert isclose( #isclose(): verifica se os totais são aproximadamente iguais, tolerando pequenas diferenças da representação decimal de float64.
    vendas_por_categoria['valor_vendido'].sum(),
    total_vendido,
    rel_tol=1e-9, # Desativa a tolerância proporcional.
    abs_tol=0.01 # Permite até R$ 0,01 de diferença.
)

vendas_por_categoria['participacao_percentual'] = vendas_por_categoria['valor_vendido']/total_vendido*100

vendas_por_categoria = vendas_por_categoria.sort_values(
    'valor_vendido',
    ascending=False #ordem decrescente, do maior para o menor. se fosse True, era do menor para o maior.
)

# print(f'\nCategoria que mais vendeu: \n{vendas_por_categoria.head(10).round(2).to_string()}')
# print(f'\nValor vendido "Sem Categoria" \n{vendas_por_categoria.loc[['Sem categoria']].round(2).to_string()}')


assert vendas_mensais['quantidade_pedidos'].gt(0).all() #gt(0) garante que não havera divisões por zero 

vendas_mensais['ticket_medio'] = (vendas_mensais['valor_vendido'] / vendas_mensais['quantidade_pedidos'])

# print(f'\nTicket medio mensal: \n{vendas_mensais[['valor_vendido','quantidade_pedidos','ticket_medio']].round(2).to_string()}')

ticket_comparavel = vendas_mensais.loc[
    "2017-02":"2018-07"
].copy()

mes_maior_ticket = ticket_comparavel["ticket_medio"].idxmax()
mes_menor_ticket = ticket_comparavel["ticket_medio"].idxmin()

# print(f'\nMaior ticket médio: \n{ticket_comparavel.loc[mes_maior_ticket]}')
# print(f'\nMenor ticket médio: \n{ticket_comparavel.loc[mes_menor_ticket]}')
