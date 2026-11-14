from pathlib import Path

import matplotlib.pyplot as plt
from graficos.formatacao import brasileiro, contextualizar


def criar_grafico_pagamentos(resumo_formas, resumo_parcelamento):
    formas = resumo_formas.sort_values("participacao_valor")
    parcelas = resumo_parcelamento.loc[resumo_parcelamento.index <= 10].sort_index()

    assert not formas.empty
    assert not parcelas.empty
    assert parcelas[
        ["quantidade_pedidos", "valor_medio_compra", "valor_mediano_compra"]
    ].notna().all().all()

    fig, eixos = plt.subplots(
        3, 1,
        figsize=(13, 12),
        layout="constrained",
    )

    fig.suptitle("Formas de pagamento e parcelamento", fontsize=17)

    # Participação de cada forma no valor pago.
    ax = eixos[0]

    nomes_formas = {
        "credit_card": "Cartão de crédito",
        "boleto": "Boleto",
        "voucher": "Voucher",
        "debit_card": "Cartão de débito",
    }

    rotulos_formas = [
        nomes_formas.get(forma, forma)
        for forma in formas.index
    ]

    barras = ax.barh(
        rotulos_formas,
        formas["participacao_valor"],
        color="#287D8E",
    )

    ax.bar_label(barras, padding=4, fmt="%.2f%%")
    ax.set_xlim(0, 100)
    ax.set_title("Cartão de crédito concentra a maior parte do valor pago")
    ax.set_xlabel("Participação no valor pago registrado (%)")

    # Média e mediana da compra por quantidade de parcelas.
    ax = eixos[1]

    ax.plot(
        parcelas.index,
        parcelas["valor_medio_compra"],
        marker="o",
        color="#287D8E",
        label="Média", linestyle='None',
    )

    ax.plot(
        parcelas.index,
        parcelas["valor_mediano_compra"],
        marker="o",
        color="#C45136",
        label="Mediana", linestyle='None', markerfacecolor='none',
    )

    destaques = parcelas.loc[[8, 10]]

    ax.scatter(
        destaques.index,
        destaques["valor_medio_compra"],
        s=100,
        facecolors="none",
        edgecolors="#333333",
        linewidths=1.5,
        zorder=3,
    )

    ax.set_title(
        "Oito e dez parcelas combinam valores elevados e milhares de pedidos"
    )
    ax.set_ylabel("Valor total pago por compra (R$)")
    ax.set_ylim(bottom=0)
    ax.legend()

    # Quantidade de pedidos que sustenta cada comparação.
    ax = eixos[2]

    cores = [
        "#C45136" if parcela in [8, 10] else "#287D8E"
        for parcela in parcelas.index
    ]

    barras = ax.bar(
        parcelas.index,
        parcelas["quantidade_pedidos"],
        color=cores,
    )

    ax.bar_label(barras, padding=4, fmt="%.0f", fontsize=8)
    ax.set_ylim(
        0,
        parcelas["quantidade_pedidos"].max() * 1.2,
    )
    ax.set_title("Quantos pedidos sustentam cada grupo?")
    ax.set_ylabel("Pedidos")
    ax.set_xlabel("Quantidade de parcelas")

    eixos[1].set_xticks(parcelas.index)
    eixos[2].set_xticks(parcelas.index)
    eixos[1].set_xlim(0.5, parcelas.index.max() + 0.5)
    eixos[2].set_xlim(0.5, parcelas.index.max() + 0.5)

    fig.supxlabel(
        "Parcelamento: pedidos entregues com pagamento único no cartão, "
        "parcelas válidas e valor positivo.",
        fontsize=10,
    )

    pasta_imagens = (
        Path(__file__).resolve().parent.parent / "web" / "imagens"
    )
    pasta_imagens.mkdir(parents=True, exist_ok=True)

    caminho_imagem = pasta_imagens / "grafico_pagamentos.png"

    raros = resumo_parcelamento.loc[resumo_parcelamento.index > 10, 'quantidade_pedidos'].sum()
    fig.suptitle(f'Oito e dez parcelas combinam valor e volume no cartão único\nAcima de dez: {brasileiro(raros, 0)} pedidos ({brasileiro(raros / resumo_parcelamento["quantidade_pedidos"].sum() * 100)}%); detalhes na tabela', fontsize=15)
    contextualizar(fig, '09/2016–08/2018; cartão único, parcelas ≥ 1 e valor positivo')
    fig.savefig(caminho_imagem, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return caminho_imagem
