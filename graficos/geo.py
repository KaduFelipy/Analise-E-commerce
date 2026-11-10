from pathlib import Path

import matplotlib.pyplot as plt


def criar_grafico_geo(resumo_estados):
    top_clientes = resumo_estados.nlargest(5, "clientes_distintos")
    top_vendas = resumo_estados.nlargest(5, "valor_produtos")
    top_frete = resumo_estados.nlargest(5, "frete_percentual")

    fig, eixos = plt.subplots(3, 1, figsize=(11, 10), layout="constrained")
    fig.suptitle("Distribuição geográfica dos pedidos entregues")

    ax = eixos[0]
    barras = ax.barh(
        top_clientes.index, top_clientes["clientes_distintos"], color="#287D8E"
    )
    ax.bar_label(barras, padding=4, fmt="%.0f")
    ax.set_title("Onde estão os maiores números de clientes?")
    ax.set_xlabel("Clientes distintos no estado")

    ax = eixos[1]
    barras = ax.barh(
        top_vendas.index, top_vendas["valor_produtos"] / 1_000_000, color="#287D8E"
    )
    ax.bar_label(barras, padding=4, fmt="%.2f")
    ax.set_title("Onde o valor vendido é maior?")
    ax.set_xlabel("Valor dos produtos (R$ milhões, sem frete)")

    rotulos_frete = [
        f"{estado} ({pedidos} pedidos)"
        for estado, pedidos in top_frete["pedidos_distintos"].items()
    ]

    ax = eixos[2]
    barras = ax.barh(
        rotulos_frete, top_frete["frete_percentual"], color="#C45136"
    )
    ax.bar_label(barras, padding=4, fmt="%.2f%%")
    ax.set_title("Onde o frete pesa mais sobre o valor dos produtos?")
    ax.set_xlabel("Frete total ÷ valor dos produtos (%)")

    for ax in eixos:
        ax.invert_yaxis()
        ax.margins(x=0.20)

    pasta_imagens = Path(__file__).resolve().parent.parent / "web" / "imagens"
    pasta_imagens.mkdir(parents=True, exist_ok=True)

    caminho_imagem = pasta_imagens / "grafico_geografia.png"
    fig.savefig(caminho_imagem, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return caminho_imagem