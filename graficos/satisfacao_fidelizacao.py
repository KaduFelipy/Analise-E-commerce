from pathlib import Path

import matplotlib.pyplot as plt


def criar_grafico_satisfacao_fidelizacao(
    resumo_satisfacao,
    resumo_recorrencia,
):
    satisfacao = resumo_satisfacao.reindex([False, True])
    recorrencia = resumo_recorrencia.reindex([False, True])

    assert satisfacao["nota_media"].notna().all()
    assert recorrencia[
        ["ticket_medio", "valor_por_cliente"]
    ].notna().all().all()

    fig, eixos = plt.subplots(
        3, 1,
        figsize=(12, 12),
        layout="constrained",
    )

    fig.suptitle(
        "Satisfação e recorrência de compra",
        fontsize=17,
    )

    # Avaliações dos pedidos com nota disponível.
    ax = eixos[0]

    barras = ax.bar(
        ["No prazo", "Atrasados"],
        satisfacao["nota_media"].to_numpy(),
        color=["#287D8E", "#C45136"],
        width=0.5,
    )

    rotulos_notas = [
        f"{nota:.2f} | {quantidade} pedidos avaliados"
        for nota, quantidade in zip(
            satisfacao["nota_media"],
            satisfacao["pedidos_com_nota"],
        )
    ]

    ax.bar_label(barras, labels=rotulos_notas, padding=5)
    ax.set_ylim(0, 5.7)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_ylabel("Nota média")
    ax.set_title("Pedidos atrasados receberam avaliações menores")

    # Participação somente do grupo recorrente.
    ax = eixos[1]

    participacoes = [
        recorrencia.loc[True, "participacao_clientes"],
        recorrencia.loc[True, "participacao_valor"],
    ]

    barras = ax.bar(
        ["Entre os clientes", "No valor vendido"],
        participacoes,
        color=["#287D8E", "#C45136"],
        width=0.5,
    )

    ax.bar_label(barras, padding=5, fmt="%.2f%%")
    ax.set_ylim(0, max(participacoes) * 1.4)
    ax.set_ylabel("Participação (%)")
    ax.set_title(
        "Recorrentes representam 3% dos clientes e 5,51% do valor vendido"
    )

    # Comparação entre valor por pedido e valor por cliente.
    ax = eixos[2]

    barras_ticket = ax.bar(
        [-0.18, 0.82],
        recorrencia["ticket_medio"].to_numpy(),
        width=0.36,
        color="#287D8E",
        label="Ticket médio por pedido",
    )

    barras_cliente = ax.bar(
        [0.18, 1.18],
        recorrencia["valor_por_cliente"].to_numpy(),
        width=0.36,
        color="#C45136",
        label="Valor acumulado por cliente",
    )

    ax.bar_label(barras_ticket, padding=4, fmt="%.2f")
    ax.bar_label(barras_cliente, padding=4, fmt="%.2f")
    ax.set_xticks(
        [0, 1],
        ["Uma compra entregue", "Duas ou mais compras entregues"],
    )
    ax.set_ylim(
        0,
        recorrencia[["ticket_medio", "valor_por_cliente"]]
        .max()
        .max() * 1.35,
    )
    ax.set_ylabel("Valor dos produtos (R$, sem frete)")
    ax.set_title("A repetição de compras aumenta o valor acumulado por cliente")
    ax.legend(loc="upper left")

    pasta_imagens = (
        Path(__file__).resolve().parent.parent / "web" / "imagens"
    )
    pasta_imagens.mkdir(parents=True, exist_ok=True)

    caminho_imagem = pasta_imagens / "grafico_satisfacao_fidelizacao.png"

    fig.savefig(caminho_imagem, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return caminho_imagem