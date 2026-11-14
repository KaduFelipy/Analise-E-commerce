from pathlib import Path

import matplotlib.pyplot as plt
from graficos.formatacao import contextualizar, brasileiro


def criar_grafico_geo(resumo_estados):
    top_clientes = resumo_estados.nlargest(5, "valor_produtos")
    top_vendas = resumo_estados.nlargest(5, "valor_produtos")
    top_frete = resumo_estados.nlargest(5, "frete_percentual")

    fig, eixos = plt.subplots(3, 1, figsize=(11, 10), layout="constrained")
    fig.suptitle("Distribuição geográfica dos pedidos entregues")

    ax = eixos[0]
    barras = ax.barh(
        top_clientes.index, top_clientes["participacao_vendas"], color="#287D8E"
    )
    ax.bar_label(barras, padding=4, fmt=lambda v: brasileiro(v) + '%')
    ax.set_title("Cinco destinos com maior participação nas vendas")
    ax.set_xlabel("Participação no valor dos produtos (%) — demais UFs na tabela")

    ax = eixos[1]
    ax.scatter(top_vendas['ticket_medio'], top_vendas.index, label='Ticket', marker='o', color='#287D8E')
    ax.scatter(top_vendas['frete_medio_pedido'], top_vendas.index, label='Frete médio', marker='s', color='#C45136')
    ax.set_xlim(left=0)
    ax.set_title("Ticket e frete registrado nos mesmos destinos")
    ax.set_xlabel("Reais por pedido entregue (R$)")
    ax.legend()

    rotulos_frete = [
        f"{estado} ({pedidos} pedidos)"
        for estado, pedidos in top_frete["pedidos_distintos"].items()
    ]

    ax = eixos[2]
    barras = ax.barh(
        rotulos_frete, top_frete["frete_percentual"], color="#C45136"
    )
    ax.bar_label(barras, padding=4, fmt=lambda v: brasileiro(v) + '%')
    ax.set_title("Onde o frete pesa mais sobre o valor dos produtos?")
    ax.set_xlabel("Frete total ÷ valor dos produtos (%)")

    for ax in eixos:
        ax.invert_yaxis()
        ax.margins(x=0.20)

    pasta_imagens = Path(__file__).resolve().parent.parent / "web" / "imagens"
    pasta_imagens.mkdir(parents=True, exist_ok=True)

    caminho_imagem = pasta_imagens / "grafico_geografia.png"
    contextualizar(fig, '09/2016–08/2018; pedidos entregues')
    fig.savefig(caminho_imagem, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return caminho_imagem
