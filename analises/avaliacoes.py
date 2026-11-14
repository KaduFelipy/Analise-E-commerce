from pathlib import Path
import pandas as pd

raiz_projeto = Path(__file__).resolve().parent.parent
pasta_dados = raiz_projeto / 'dados' / 'olist'
caminho_avaliacoes = pasta_dados / 'olist_order_reviews_dataset.csv'

avaliacoes = pd.read_csv(caminho_avaliacoes)

for coluna in ['review_creation_date', 'review_answer_timestamp']:
    avaliacoes[coluna] = pd.to_datetime(avaliacoes[coluna], errors='raise')

qualidade_datas = avaliacoes[['review_creation_date', 'review_answer_timestamp']].isna().sum()
respostas_antes_criacao = (avaliacoes['review_answer_timestamp'] < avaliacoes['review_creation_date']).sum()


def classificar_momento(registros):
    r = registros.copy()
    resposta = r['review_answer_timestamp']
    entrega = r['order_delivered_customer_date']
    r['momento_resposta'] = 'Não classificável'
    validos = resposta.notna() & entrega.notna()
    r.loc[validos & (resposta < entrega), 'momento_resposta'] = 'Antes da entrega'
    r.loc[validos & (resposta >= entrega), 'momento_resposta'] = 'Na entrega ou depois'
    r['espera_apos_prazo'] = (
        (r['momento_resposta'] == 'Antes da entrega')
        & (resposta.dt.normalize() > r['order_estimated_delivery_date'].dt.normalize())
    )
    return r


# print(f'\nPrimeiras avaliacoes \n{avaliacoes.head().to_string(index=False)}')
# print(f'\nLinhas e colunas da tabela \n{avaliacoes.shape}')
# print(f'\nColunas das avaliacoes \n{avaliacoes.columns.tolist()}')
# print(f'\nCampos ausentes avaliacoes \n{avaliacoes[['order_id','review_score']].isna().sum()}')
# print(f'\nDistribuicao das avaliacoes \n{avaliacoes['review_score'].value_counts(dropna=False).sort_index()}')
