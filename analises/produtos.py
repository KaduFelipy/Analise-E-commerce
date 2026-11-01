from pathlib import Path
import pandas as pd

raiz_projeto = Path(__file__).resolve().parent.parent

pasta_dados=(
    raiz_projeto
    /'dados'
    /'olist'
)

produtos = pd.read_csv(
    pasta_dados / 'olist_products_dataset.csv'
)
if __name__ == '__main__':
    # print(f'\nPré visualização \n{produtos.head().to_string(index=False)}')
    # print(f'\nColunas das tabelas \n{produtos.columns.tolist()}')

    print(f'\nProdutos ausentes: \n{produtos['product_id'].isna().sum()}')
    print(f'\nProdutos duplicados: \n{produtos['product_id'].duplicated().sum()}')
    print(f'\nCategoria ausentes: \n{produtos['product_category_name'].isna().sum()}')