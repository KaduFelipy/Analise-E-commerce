from analises.vendas import vendas_mensais
from graficos.vendas import criar_grafico_vendas
from analises.entregas import pedidos_analisados, resumo_estados
from graficos.entregas import criar_grafico_entregas
from pathlib import Path
import webbrowser


caminho_grafico_entregas = criar_grafico_entregas(
    pedidos_analisados, resumo_estados
)

caminho_grafico_vendas = criar_grafico_vendas(vendas_mensais)


caminho_html = (
    Path(__file__).resolve().parent
    /'web'
    /'index.html'
)

if not caminho_grafico_entregas.is_file():
    raise FileNotFoundError(f'Página não encontrada!')

if not caminho_grafico_vendas.is_file():
    raise FileNotFoundError(f'Página não encontrada!')

webbrowser.open(caminho_html.as_uri())