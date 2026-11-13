from pathlib import Path
import pandas as pd

raiz_projeto = Path(__file__).resolve().parent.parent
pasta_dados = raiz_projeto / 'dados' / 'olist'
caminho_avaliacoes = pasta_dados / 'olist_order_reviews_dataset.csv'

avaliacoes = pd.read_csv(caminho_avaliacoes)


# print(f'\nPrimeiras avaliacoes \n{avaliacoes.head().to_string(index=False)}')
# print(f'\nLinhas e colunas da tabela \n{avaliacoes.shape}')
# print(f'\nColunas das avaliacoes \n{avaliacoes.columns.tolist()}')
# print(f'\nCampos ausentes avaliacoes \n{avaliacoes[['order_id','review_score']].isna().sum()}')
# print(f'\nDistribuicao das avaliacoes \n{avaliacoes['review_score'].value_counts(dropna=False).sort_index()}')
