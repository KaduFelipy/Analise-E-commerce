from pathlib import Path
import webbrowser

from analises.vendas import vendas_mensais
from graficos.vendas import criar_grafico_vendas

from analises.entregas import pedidos_analisados, resumo_estados
from graficos.entregas import criar_grafico_entregas

from analises.geo import resumo_estados as resumo_geo
from graficos.geo import criar_grafico_geo

from analises.vendedores import resumo_vendedores
from graficos.vendedores import criar_grafico_vendedores






caminho_grafico_entregas = criar_grafico_entregas(
    pedidos_analisados, resumo_estados
)

caminho_grafico_vendas = criar_grafico_vendas(vendas_mensais)

caminho_grafico_geo = criar_grafico_geo(resumo_geo)

caminho_grafico_vendedores = criar_grafico_vendedores(
    pedidos_analisados,
    resumo_vendedores
)


caminho_html = (
    Path(__file__).resolve().parent
    /'web'
    /'index.html'
)

if not caminho_grafico_entregas.is_file():
    raise FileNotFoundError(f'Página não encontrada!')

if not caminho_grafico_vendas.is_file():
    raise FileNotFoundError(f'Página não encontrada!')

if not caminho_grafico_geo.is_file():
    raise FileNotFoundError(f'Página não encontrada!')

if not caminho_grafico_vendedores.is_file():
    raise FileNotFoundError(f'Página não encontrada!')

webbrowser.open(caminho_html.as_uri())