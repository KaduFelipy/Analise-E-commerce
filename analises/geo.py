from pathlib import Path
import pandas as pd

from analises.clientes import clientes
from analises.vendas import itens_vendidos

raiz_projeto = Path(__file__).resolve().parent.parent

pasta_dados = (
    raiz_projeto
    /'dados'
    /'olist'
)

geolocation = pd.read_csv(
    pasta_dados / 'olist_geolocation_dataset.csv'
)

fretes_negativos = (itens_vendidos['freight_value'] < 0).sum()

# print(f'\n Pré visualização \n {geolocation.head().to_string(index=False)}')
# print(f'\n Colunas da tabela \n {geolocation.columns.tolist()}')

# print(f'\nCampos ausentes nos clientes \n {clientes[['customer_id','customer_unique_id','customer_state']].isna().sum()}')
# print(f'\nClientes repetidos \n {clientes[['customer_id']].duplicated().sum()}')
# print(f'\nItens vendidos \n {itens_vendidos[['order_id','customer_id','price','freight_value']].isna().sum()}')
# print(f'\nTipo da Coluna Frete \n {itens_vendidos['freight_value'].dtype}')
# print(f'\nFrete negativos \n {fretes_negativos}')

itens_por_estado = itens_vendidos.merge(
    clientes[['customer_id', 'customer_unique_id', 'customer_state']],
    on='customer_id',
    how='left',
    validate='many_to_one'
)

assert len(itens_por_estado) == len(itens_vendidos)
assert itens_por_estado['customer_state'].notna().all()

resumo_estados = itens_por_estado.groupby('customer_state').agg(
    clientes_distintos = ('customer_unique_id','nunique'),
    pedidos_distintos = ('order_id','nunique'),
    valor_produtos = ('price','sum'),
    valor_frete = ('freight_value', 'sum')
)

assert resumo_estados['valor_produtos'].gt(0).all()

# print(f'\nCinco estados com mais clientes \n{resumo_estados.nlargest(5,'clientes_distintos').round(2)}')
# print(f'\nCinco estados com maior valor vendido \n{resumo_estados.nlargest(5,'valor_produtos').round(2)}')

resumo_estados['frete_percentual'] = (
    resumo_estados['valor_frete'] / resumo_estados['valor_produtos'] * 100
)
maiores_proporcoes = resumo_estados.nlargest(5,'frete_percentual')[['pedidos_distintos', 'valor_produtos','valor_frete','frete_percentual']]

from analises.entregas import resumo_estados as entregas_estados

resumo_integrado = resumo_estados.join(entregas_estados.rename(columns={'pedidos_entregues': 'pedidos_avaliaveis'}), validate='one_to_one')
resumo_integrado['participacao_vendas'] = resumo_integrado['valor_produtos'] / resumo_integrado['valor_produtos'].sum() * 100
resumo_integrado['ticket_medio'] = resumo_integrado['valor_produtos'] / resumo_integrado['pedidos_distintos']
resumo_integrado['frete_medio_pedido'] = resumo_integrado['valor_frete'] / resumo_integrado['pedidos_distintos']

# print(f'\nCinco estados com maior proporção de frete \n{maiores_proporcoes.round(2).to_string()}')


