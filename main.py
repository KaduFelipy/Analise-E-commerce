from analises.entregas import pedidos_analisados, resumo_estados
from graficos.entregas import criar_grafico_entregas
from pathlib import Path
import webbrowser


caminho_imagem = criar_grafico_entregas(
    pedidos_analisados, resumo_estados
)

caminho_html = (
    Path(__file__).resolve().parent
    /'web'
    /'index.html'
)

if not caminho_imagem.is_file():
    raise FileNotFoundError(f'Página não encontrada!')

webbrowser.open(caminho_html.as_uri())