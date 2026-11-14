from pathlib import Path

import matplotlib.pyplot as plt

from graficos.formatacao import brasileiro, contextualizar


def criar_grafico_satisfacao_fidelizacao(resumo_satisfacao, resumo_recorrencia, resumo_recompra, resumo_momento):
    pasta = Path(__file__).resolve().parent.parent / 'web' / 'imagens'
    pasta.mkdir(parents=True, exist_ok=True)
    caminhos = []
    fig, ax = plt.subplots(figsize=(11, 6), layout='constrained')
    dados = resumo_momento.reset_index()
    rotulos = [('Atrasado' if r.atrasados else 'No prazo') + '\n' + r.recorte_resposta.replace(', ', '\n') for r in dados.itertuples()]
    barras = ax.barh(rotulos, dados['nota_media'], color=['#C45136' if v else '#287D8E' for v in dados['atrasados']])
    ax.bar_label(barras, labels=[f'{brasileiro(r.nota_media)} | n={brasileiro(r.pedidos, 0)}' for r in dados.itertuples()], padding=4)
    ax.set_xlim(0, 6.2)
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_xlabel('Nota média por pedido e recorte (escala 1–5); n = pedidos')
    principais = resumo_momento.loc[True]
    ax.set_title(f'Pedidos atrasados: espera após prazo {brasileiro(principais.loc["Antes da entrega, após o dia prometido", "nota_media"])} vs. entrega/depois {brasileiro(principais.loc["Na entrega ou depois", "nota_media"])}')
    contextualizar(fig, '09/2016–08/2018; prazo avaliável; pedidos podem aparecer em vários recortes')
    caminho = pasta / 'grafico_satisfacao_fidelizacao.png'
    fig.savefig(caminho, dpi=150, bbox_inches='tight')
    plt.close(fig)
    caminhos.append(caminho)

    fig, eixos = plt.subplots(1, 1, figsize=(10, 4), layout='constrained')
    valores = resumo_recompra[['multiplos_pedidos', 'outro_dia']]
    barras = eixos.barh(['Múltiplos pedidos entregues', 'Compras em dias diferentes'], valores, color='#287D8E')
    eixos.bar_label(barras, labels=[brasileiro(v, 0) for v in valores], padding=4)
    eixos.set_xlim(0, valores.max() * 1.25)
    eixos.set_xlabel('Clientes distintos; indicadores diferentes')
    eixos.set_title('Múltiplos pedidos não demonstram retorno em outro dia')
    contextualizar(fig, '09/2016–08/2018; pedidos entregues; cobertura não comprova completude')
    caminho = pasta / 'grafico_recompra.png'
    fig.savefig(caminho, dpi=150, bbox_inches='tight')
    plt.close(fig)
    caminhos.append(caminho)
    return caminhos

