from pathlib import Path
import argparse
import webbrowser

from analises import entregas, vendas, geo, vendedores
from analises import satisfacao_fidelizacao as satisfacao, pagamentos
from graficos.entregas import criar_grafico_entregas
from graficos.vendas import criar_grafico_vendas, criar_grafico_contribuicoes
from graficos.geo import criar_grafico_geo
from graficos.vendedores import criar_grafico_vendedores
from graficos.satisfacao_fidelizacao import criar_grafico_satisfacao_fidelizacao
from graficos.pagamentos import criar_grafico_pagamentos
from web.relatorio import gerar_relatorio


def main():
    parser = argparse.ArgumentParser(description='Regenera figuras, tabelas e relatório Olist.')
    parser.add_argument('--sem-abrir', action='store_true', help='Gera a entrega sem abrir o navegador.')
    argumentos = parser.parse_args()
    caminhos = [
        criar_grafico_entregas(entregas.pedidos_analisados, entregas.resumo_estados),
        criar_grafico_vendas(vendas.vendas_mensais),
        criar_grafico_contribuicoes(vendas.contribuicoes_categorias),
        criar_grafico_geo(geo.resumo_integrado),
        criar_grafico_vendedores(entregas.pedidos_analisados, vendedores.resumo_vendedores),
        criar_grafico_pagamentos(pagamentos.resumo_formas, pagamentos.resumo_parcelamento),
    ]
    caminhos.extend(criar_grafico_satisfacao_fidelizacao(
        satisfacao.resumo_satisfacao, satisfacao.resumo_recorrencia,
        satisfacao.resumo_recompra, satisfacao.resumo_momento,
    ))
    caminho_html = gerar_relatorio()
    for caminho in [*caminhos, caminho_html]:
        if not Path(caminho).is_file():
            raise FileNotFoundError(caminho)
    print(f'Geradas {len(caminhos)} figuras, tabelas e página: {caminho_html}')
    if not argumentos.sem_abrir:
        webbrowser.open(caminho_html.as_uri())


if __name__ == '__main__':
    main()
