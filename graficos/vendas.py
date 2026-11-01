from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def criar_grafico_vendas(vendas_mensais):
    periodo = vendas_mensais.loc["2017-02":"2018-07"].copy()

    assert not periodo.empty
    assert periodo[
        ["valor_vendido", "quantidade_pedidos", "ticket_medio"]
    ].notna().all().all()

    meses = periodo.index.astype(str)

    fig, eixos = plt.subplots(
        3, 1,
        figsize=(13, 10),
        sharex=True,
        layout="constrained",
    )

    fig.suptitle(
        "Valor vendido, volume de pedidos e ticket médio\n"
        "Produtos de pedidos entregues, sem frete",
        fontsize=16,
    )

    eixos[0].plot(
        meses,
        periodo["valor_vendido"],
        marker="o",
        color="#287D8E",
    )
    eixos[0].set_title("Como o valor vendido evoluiu?")
    eixos[0].set_ylabel("Valor vendido (R$)")
    eixos[0].yaxis.set_major_formatter(
        FuncFormatter(
            lambda valor, posicao: f"{valor:,.0f}".replace(",", ".")
        )
    )

    eixos[1].bar(
        meses,
        periodo["quantidade_pedidos"],
        color="#287D8E",
    )
    eixos[1].set_title("Como variou a quantidade de pedidos?")
    eixos[1].set_ylabel("Pedidos")

    eixos[2].plot(
        meses,
        periodo["ticket_medio"],
        marker="o",
        color="#C45136",
    )
    eixos[2].set_title("Como variou o valor médio por pedido?")
    eixos[2].set_ylabel("Ticket médio (R$)")
    eixos[2].set_ylim(bottom=0)
    eixos[2].set_xlabel("Mês da compra")
    eixos[2].tick_params(axis="x", labelrotation=45)

    raiz_projeto = Path(__file__).resolve().parent.parent
    pasta_imagens = raiz_projeto / "web" / "imagens"
    pasta_imagens.mkdir(parents=True, exist_ok=True)

    caminho_imagem = pasta_imagens / "grafico_vendas_mensais.png"

    fig.savefig(
        caminho_imagem,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(fig)

    return caminho_imagem