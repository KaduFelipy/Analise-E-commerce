from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from graficos.formatacao import brasileiro, contextualizar


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

    for ax, coluna in zip(eixos, ['valor_vendido', 'quantidade_pedidos', 'ticket_medio']):
        valores = periodo.loc['2017-11':'2017-12', coluna]
        mudanca = (valores.iloc[1] / valores.iloc[0] - 1) * 100
        ax.axvspan(9, 10, alpha=.12, color='#C45136')
        ax.annotate(f'Nov → dez/2017: {brasileiro(mudanca)}%', xy=(10, valores.iloc[1]), xytext=(20, 24), textcoords='offset points', arrowprops={'arrowstyle': '->'}, fontsize=9)
    contextualizar(fig, '02/2017–07/2018; pedidos entregues')
    fig.savefig(
        caminho_imagem,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(fig)

    return caminho_imagem


def criar_grafico_contribuicoes(contribuicoes):
    import pandas as pd

    negativos = contribuicoes.loc[contribuicoes['diferenca_reais'] < 0].head(8)
    positivos = contribuicoes.loc[contribuicoes['diferenca_reais'] > 0].tail(4)
    destaque = pd.concat([negativos, positivos])['diferenca_reais'].copy()
    restante = contribuicoes['diferenca_reais'].sum() - destaque.sum()
    destaque.loc['Demais categorias (saldo)'] = restante
    fig, ax = plt.subplots(figsize=(12, 7), layout='constrained')
    from web.relatorio import nome
    barras = ax.barh([nome(x) for x in destaque.index], destaque, color=['#8a9b9d' if i == len(destaque)-1 else '#C45136' if x < 0 else '#287D8E' for i, x in enumerate(destaque)])
    ax.invert_yaxis()
    ax.bar_label(barras, labels=[brasileiro(x) for x in destaque], padding=4, fontsize=9)
    ax.axvline(0, color='#333', linewidth=.8)
    ax.margins(x=.35)
    ax.set_xlabel('Diferença em R$: dezembro menos novembro; aumentos compensam reduções')
    ax.set_title('Categorias compõem a queda; aumentos também são preservados')
    contextualizar(fig, '11/2017 → 12/2017; produtos de pedidos entregues, sem frete')
    caminho = Path(__file__).resolve().parent.parent / 'web' / 'imagens' / 'grafico_contribuicoes.png'
    caminho.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(caminho, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return caminho
