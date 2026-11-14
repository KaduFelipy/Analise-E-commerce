from pathlib import Path

import matplotlib.pyplot as plt
from graficos.formatacao import brasileiro, contextualizar


def criar_grafico_vendedores(pedidos_analisados, resumo_vendedores):
    assert len(pedidos_analisados) > 0

    taxa_geral_atraso = pedidos_analisados["atrasados"].mean() * 100
    taxa_no_prazo = 100 - taxa_geral_atraso

    ranking = resumo_vendedores.sort_values(
        ["pedidos_atrasados", "taxa_atraso"],
        ascending=[False, False],
    ).head(10)

    fig, eixos = plt.subplots(
        1, 2,
        figsize=(16, 7),
        sharey=True,
        layout="constrained",
    )

    fig.suptitle(
        f"Entregas no prazo: {taxa_no_prazo:.2f}%\n"
        "Dez vendedores com mais pedidos associados a atrasos",
        fontsize=16,
    )

    ax = eixos[0]

    barras = ax.barh(
        ranking['rotulo'],
        ranking["pedidos_atrasados"],
        color="#287D8E",
    )

    ax.bar_label(barras, padding=4, fmt="%.0f")
    ax.set_xlim(0, ranking["pedidos_atrasados"].max() * 1.25)
    ax.set_title("Quantidade de pedidos atrasados")
    ax.set_xlabel("Pedidos")
    ax.set_ylabel("Identificador do vendedor")
    ax.tick_params(axis="y", labelsize=8)
    ax.invert_yaxis()

    ax = eixos[1]

    barras = ax.barh(
        ranking['rotulo'],
        ranking["taxa_atraso"],
        color="#C45136",
    )

    rotulos = [
        f"{brasileiro(taxa)}% | {brasileiro(pedidos, 0)} avaliáveis"
        for taxa, pedidos in zip(
            ranking["taxa_atraso"],
            ranking["pedidos_avaliados"],
        )
    ]

    for y, rotulo in enumerate(rotulos):
        ax.text(ranking['taxa_atraso'].max() * 1.05, y, rotulo, va='center', fontsize=8, bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 1})
    ax.set_xlim(0, ranking["taxa_atraso"].max() * 1.8)
    ax.set_title("Taxa de atraso dos mesmos vendedores")
    ax.set_xlabel("Pedidos atrasados / pedidos avaliados (%)")

    ax.axvline(
        taxa_geral_atraso,
        color="#333333",
        linestyle="--",
        label=f"Referência geral: {taxa_geral_atraso:.2f}%",
    )

    ax.legend(loc="lower right", fontsize=8)

    pasta_imagens = (
        Path(__file__).resolve().parent.parent / "web" / "imagens"
    )
    pasta_imagens.mkdir(parents=True, exist_ok=True)

    caminho_imagem = pasta_imagens / "grafico_vendedores.png"

    contextualizar(fig, f"{pedidos_analisados['order_purchase_timestamp'].min():%m/%Y}–{pedidos_analisados['order_purchase_timestamp'].max():%m/%Y}")
    fig.savefig(caminho_imagem, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return caminho_imagem
