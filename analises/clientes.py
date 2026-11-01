from pathlib import Path
import pandas as pd

raiz_projeto = Path(__file__).resolve().parent.parent 
caminho_clientes = (
    raiz_projeto
    /'dados'#aqui ele adiciona o path da pasta com dados. ex: pasta\dados
    /'olist'# e assim por diante. ex: pasta\dados\olist
    /'olist_customers_dataset.csv'
)

clientes = pd.read_csv(caminho_clientes)