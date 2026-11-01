import matplotlib.pyplot as plt
from pathlib import Path

def criar_grafico_entregas(pedidos_analisados, resumo_estados):
    total = len(pedidos_analisados)
    quantidade_atrasados = pedidos_analisados['atrasados'].sum()
    taxa_geral = quantidade_atrasados / total * 100

    dias_atraso = pedidos_analisados.loc[
        pedidos_analisados['atrasados'], 'dias_apos_prazo'
    ]

    estados = resumo_estados.sort_values('pedidos_atrasados')

    fig, eixos = plt.subplots(
        2,2,
        figsize=(15,12),
        layout='constrained'
    )

    fig.suptitle(
        'Entregas: Frequência, duração e concentração dos atrasos\n'
        f'Base: {total:,} pedidos entregues com datas preenchidas',
        fontsize=17
    )

    ax = eixos[0,0]

    quantidades = [
        total - quantidade_atrasados,
        quantidade_atrasados
    ]

    barras = ax.bar(
        ['No prazo', 'Atrasados'],
        quantidades,
        color = ['#287D8E','#C45136']
    )

    ax.bar_label(barras, padding=4,fmt='%.0f')
    ax.set_ylim(0,max(quantidades)*1.15)
    ax.set_ylabel('Quantidade de pedidos')
    ax.set_title(f'{taxa_geral:.2f}% das entregas chegaram após o prazo')

    ax = eixos[0,1]

    ax.hist(
        dias_atraso,
        bins=range(0,int(dias_atraso.max())+6,5),
        color='#287D8E',
        edgecolor='white'
        )

    ax.axvline(
        dias_atraso.mean(),
        color='#C45136',
        linestyle='--',
        label=f'Média: {dias_atraso.mean():.2f} dias'
    )

    ax.axvline(
        dias_atraso.median(),
        color='#333333',
        linestyle=':',
        label=f'Mediana: {dias_atraso.median():.0f} dias'
    )

    ax.set_title('Quanto duraram os atrasos?')
    ax.set_xlabel('Dias após o prazo - faixas de 5 dias')
    ax.set_ylabel('Quantidade de pedidos atrasados')
    ax.legend()

    ax = eixos[1,0]

    barras = ax.barh(
        estados.index,
        estados['pedidos_atrasados'],
        color='#287D8E'
    )

    ax.bar_label(barras, padding=3, fmt='%.0f', fontsize=8)
    ax.set_xlim(0, estados['pedidos_atrasados'].max()*1.25)
    ax.set_title('Onde há mais pedidos atrasados?')
    ax.set_xlabel('Quantidade de pedidos atrasados')
    ax.set_ylabel('Estado de destino')

    ax = eixos [1,1]

    barras = ax.barh(
        estados.index,
        estados['taxa_atraso'],
        color='#C45136'
    )

    ax.bar_label(barras,padding=3,fmt='%.2f', fontsize=8)
    ax.set_xlim(0,estados['taxa_atraso'].max()*1.25)

    ax.axvline(
        taxa_geral,
        color='#333333',
        linestyle='--',
        label=f'Taxa geral: {taxa_geral:.2f}%'
    )

    ax.set_title('Onde a proporção de atrasos e maior?')
    ax.set_xlabel('Taxa de atraso (%)')
    ax.legend(loc='lower right')

    raiz_projeto = Path(__file__).resolve().parent.parent

    pasta_imagens = raiz_projeto/'web'/'imagens'
    pasta_imagens.mkdir(parents=True,exist_ok=True)

    caminho_imagem = pasta_imagens / 'grafico_entregas.png'

    fig.savefig(
        caminho_imagem,
        dpi = 150,
        bbox_inches='tight'   
    )

    plt.close(fig)

    return caminho_imagem