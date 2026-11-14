from pathlib import Path
import pandas as pd
from analises.clientes import clientes



raiz_projeto = Path(__file__).resolve().parent.parent 
caminho_entregas = (
    raiz_projeto
    /'dados'#aqui ele adiciona o path da pasta com dados. ex: pasta\dados
    /'olist'# e assim por diante. ex: pasta\dados\olist
    /'olist_orders_dataset.csv' #até chegar no arquivo. ex: pasta\dados\olist\olist_orders_dataset.csv
)

pedidos = pd.read_csv(caminho_entregas)

# print(pedidos.head()) #Mostra as 5 primeiras linhas da planilha.
# print(pedidos.shape) #Mostra o corpo da planilha em linhas e colunas.
# print(pedidos.columns.tolist()) #Lista o cabeçalho das colunas

# print('\nTipos de colunas:')
# print(pedidos.dtypes)# Verificação dos tipos de dados das colunas

# print('\nValores ausentes por coluna:')
# print(pedidos.isna().sum())# Soma de cada coluna de pedidos sem dados

# print('\nQuantidade de IDs de pedidos repetidos:')
# print(pedidos['order_id'].duplicated().sum()) #Contagem das ordens repetidas

# print('\n Quantidade de pedidos por status:')
# print(pedidos['order_status'].value_counts(dropna=False)) # Contagem da soma de cada status

# print('\n Ausencia de data de entrega por status:')
# print(
#     pd.crosstab( #Cruza as colunas, eliminando a opção de pegar colunas sem data de entrega para o cliente.
#         pedidos['order_status'],
#         pedidos['order_delivered_customer_date'].isna()
#     )
# )

entregues =  pedidos.loc[pedidos['order_status']=='delivered']
# print('\nDatas ausentes nos pedidos entregues:')
# print(
#     entregues[
#         ['order_delivered_customer_date','order_estimated_delivery_date']
#     ].isna().sum()
# )

colunas_datas = [
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
]

# print('\nTipos das colunas de datas:')
# print(pedidos[colunas_datas].dtypes)

# print('\nExemplos de datas:')
# print(pedidos[colunas_datas].head())

for coluna in colunas_datas:
    pedidos[coluna] = pd.to_datetime(
        pedidos[coluna],
        format='%Y-%m-%d %H:%M:%S',
        errors='raise'
    )

# print('\nTipos apósa a conversão:')
# print(pedidos[colunas_datas].dtypes)

# print('\nDatas ausentes apos a conversão:')
# print(pedidos[colunas_datas].isna().sum())

filtro = (
    (pedidos['order_status'] == 'delivered') &
    pedidos['order_delivered_customer_date'].notna() &
    pedidos['order_estimated_delivery_date'].notna()
)

pedidos_analisados = pedidos.loc[filtro].copy()

# print('\nQuantidade de pedidos selecionados:')
# print(len(pedidos_analisados))

assert pedidos_analisados[colunas_datas].notna().all().all() #Filtrar apenas por delivered não garante uma coerencia entre as data, usamos o assert para validar se tem as duas datas preenchidas: Data prevista e data de entrega.

#Consideramos todos os horarios com 00:00 para fazer a comparação das datas.
data_real = pedidos_analisados['order_delivered_customer_date'].dt.normalize()
data_prometida = pedidos_analisados['order_estimated_delivery_date'].dt.normalize()

# print('\nComaparação das datas:')
# print(pd.DataFrame({
#     'data_real': data_real,
#     'data_prometida': data_prometida, 
# }).head())

pedidos_analisados['atrasados'] = data_real > data_prometida

# print('\nQuantidade de pedidos atrasados')
# print(pedidos_analisados['atrasados'].value_counts())

quantidade_atrasados = pedidos_analisados['atrasados'].sum()
total_analisado = len(pedidos_analisados)

# Aqui temos a pré Porcentagem de entrega dos pedidos atrasados.
taxa_atraso = quantidade_atrasados/total_analisado * 100


#Analise de pedidos entregues antes da data do pedido
pedidos_analisados['order_purchase_timestamp'] = pd.to_datetime(
    pedidos_analisados['order_purchase_timestamp'],
    format='%Y-%m-%d %H:%M:%S',
    errors='raise'
)

# print(f'\nDatas de compras ausentes: \n{pedidos_analisados['order_purchase_timestamp'].isna().sum()}')

entrega_antes_da_compra = (
    pedidos_analisados['order_delivered_customer_date'] < pedidos_analisados['order_purchase_timestamp']
)
#Validado a não existencia dessa condição.
# print(f'\nEntregas anteriores a compra: \n{entrega_antes_da_compra.sum()}')



#Extraindo dados dos dias de atraso das entregas.
pedidos_analisados['dias_apos_prazo'] = (
    data_real - data_prometida
).dt.days


pedidos_atrasados = pedidos_analisados.loc[
    pedidos_analisados['atrasados']
].copy()

assert (pedidos_atrasados['dias_apos_prazo'] > 0).all()

# print(f'\nPedidos atrasados: \n{len(pedidos_atrasados)}')

# print(f'\nAtrasos em dias: \n{pedidos_atrasados['dias_apos_prazo'].agg(['mean','median','max'])}')



#Como a média está em 7 dias e o maior atraso foi 188 dias. É possível que os atrasos com mais de 15 dias sejam muito reduzidos. A média aumenta muito por conta desses valores muito altos.

atrasos = pedidos_atrasados['dias_apos_prazo']
maiores_atrasos = atrasos > 15
percentual_maiores_atrasos = (maiores_atrasos.sum()/ len(maiores_atrasos)) * 100

# print(maiores_atrasos.sum())
# print(percentual_maiores_atrasos)

#Agora vamos identificar os estados e depois as regiões que tem mais esses atrasos
#Eu importei os dados dos clientes de outro arquivo pra manter uma estrutura organizada e melhorar a leitura do código


# print(f'\nPré-visualização da tabela\n{clientes.head()}')
# print(f'\nColunas da tabela{clientes.columns.tolist()}')
# print(f'\nClientes ausentes\n{clientes['customer_id'].isna().sum()}')
# print(f'\nClientes repetidos \n{clientes['customer_id'].duplicated().sum()}')
# print(f'\nEstados ausentes\n{clientes['customer_state'].isna().sum()}')

pedidos_por_estado = pedidos_analisados.merge(
    clientes[['customer_id','customer_state']],
    on='customer_id',
    how='left', #Puxa sempre a tabela pedidos_analisados como referencia
    validate='many_to_one' # Exige customer_id único na tabela de clientes
)

assert len(pedidos_por_estado) == len(pedidos_analisados)

# print(f'\n Pedidos sem estado \n{pedidos_por_estado['customer_state'].isna().sum()}')

resumo_estados = pedidos_por_estado.groupby('customer_state').agg(
    pedidos_entregues = ('atrasados','size'),
    pedidos_atrasados = ('atrasados','sum')
)

resumo_estados['taxa_atraso'] = (
    resumo_estados['pedidos_atrasados'] / resumo_estados['pedidos_entregues'] * 100
)

assert resumo_estados['pedidos_entregues'].sum() == len(pedidos_por_estado)
assert resumo_estados['pedidos_atrasados'].sum() == pedidos_por_estado['atrasados'].sum()

pedidos_por_estado['mes_compra'] = pedidos_por_estado['order_purchase_timestamp'].dt.to_period('M')
pedidos_por_estado['faixa_atraso'] = pd.cut(
    pedidos_por_estado['dias_apos_prazo'], bins=[0, 7, 15, 30, float('inf')],
    labels=['1–7', '8–15', '16–30', 'Acima de 30'],
)
resumo_estado_mes = pedidos_por_estado.groupby(['customer_state', 'mes_compra']).agg(
    pedidos_avaliaveis=('order_id', 'size'), atrasados=('atrasados', 'sum'),
)
resumo_estado_mes['taxa_atraso'] = resumo_estado_mes['atrasados'] / resumo_estado_mes['pedidos_avaliaveis'] * 100
severidade_estado_mes = pedidos_por_estado.loc[pedidos_por_estado['atrasados']].groupby(
    ['customer_state', 'mes_compra'],
)['dias_apos_prazo'].agg(mediana='median', percentil_90=lambda s: s.quantile(.9))
resumo_estado_mes = resumo_estado_mes.join(severidade_estado_mes)
resumo_faixas = pedidos_por_estado.groupby('faixa_atraso', observed=False).agg(pedidos=('order_id', 'size'))
resumo_faixas['participacao_atrasados'] = resumo_faixas['pedidos'] / quantidade_atrasados * 100
concentracao_mensal = pedidos_por_estado.groupby('mes_compra').agg(
    pedidos_avaliaveis=('order_id', 'size'), atrasados=('atrasados', 'sum'),
)
concentracao_mensal['atrasados_sp_rj'] = pedidos_por_estado.loc[
    pedidos_por_estado['customer_state'].isin(['SP', 'RJ'])
].groupby('mes_compra')['atrasados'].sum()
concentracao_mensal['participacao_sp_rj'] = concentracao_mensal['atrasados_sp_rj'] / concentracao_mensal['atrasados'].replace(0, float('nan')) * 100

intervalos = {}
for nome, inicio, fim in [
    ('Compra → aprovação', 'order_purchase_timestamp', 'order_approved_at'),
    ('Aprovação → transportador', 'order_approved_at', 'order_delivered_carrier_date'),
    ('Transportador → cliente', 'order_delivered_carrier_date', 'order_delivered_customer_date'),
]:
    duracao = (pd.to_datetime(pedidos_analisados[fim]) - pd.to_datetime(pedidos_analisados[inicio])).dt.total_seconds() / 86400
    validos = duracao.loc[duracao >= 0]
    intervalos[nome] = {'validos': len(validos), 'ausentes': int(duracao.isna().sum()),
                       'negativos': int((duracao < 0).sum()), 'mediana_dias': validos.median(),
                       'percentil_90_dias': validos.quantile(.9)}
resumo_intervalos = pd.DataFrame.from_dict(intervalos, orient='index')

episodio_rj = resumo_estado_mes.loc[('RJ', slice('2018-02', '2018-03')), :].copy()
selecionado_rj = pedidos_por_estado.loc[
    pedidos_por_estado['customer_state'].eq('RJ') & pedidos_por_estado['mes_compra'].isin(pd.period_range('2018-02', '2018-03', freq='M'))
]
linhas_intervalos = []
for recorte, dados_recorte in [
    ('Geral', pedidos_por_estado),
    ('RJ fev–mar/2018 no prazo', selecionado_rj.loc[~selecionado_rj['atrasados']]),
    ('RJ fev–mar/2018 atrasados', selecionado_rj.loc[selecionado_rj['atrasados']]),
    ('RJ fev–mar/2018 acima de 30 dias', selecionado_rj.loc[selecionado_rj['dias_apos_prazo'] > 30]),
]:
    for intervalo, inicio, fim in [
        ('Compra → aprovação', 'order_purchase_timestamp', 'order_approved_at'),
        ('Aprovação → transportador', 'order_approved_at', 'order_delivered_carrier_date'),
        ('Transportador → cliente', 'order_delivered_carrier_date', 'order_delivered_customer_date'),
        ('Compra → cliente', 'order_purchase_timestamp', 'order_delivered_customer_date'),
        ('Compra → promessa', 'order_purchase_timestamp', 'order_estimated_delivery_date'),
    ]:
        dias = (pd.to_datetime(dados_recorte[fim]) - pd.to_datetime(dados_recorte[inicio])).dt.total_seconds() / 86400
        validos = dias.loc[dias >= 0]
        linhas_intervalos.append(dict(recorte=recorte, intervalo=intervalo, total_pedidos=len(dias), validos=len(validos), ausentes=int(dias.isna().sum()), negativos=int((dias < 0).sum()), mediana_dias=validos.median(), percentil_90_dias=validos.quantile(.9)))
resumo_intervalos_recortes = pd.DataFrame(linhas_intervalos).set_index(['recorte', 'intervalo'])

# print(
#     resumo_estados.sort_values(
#         'taxa_atraso', ascending=False
#     ).round(2).to_string()
# )
