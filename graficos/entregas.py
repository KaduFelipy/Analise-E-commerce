from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from graficos.formatacao import brasileiro, contextualizar


def criar_grafico_entregas(pedidos_analisados, resumo_estados):
    total = len(pedidos_analisados)
    atrasados = pedidos_analisados.loc[pedidos_analisados['atrasados'], 'dias_apos_prazo']
    estados = resumo_estados.sort_values('pedidos_atrasados')
    fig, eixos = plt.subplots(2, 2, figsize=(15, 12), layout='constrained')
    ax = eixos[0, 0]
    valores = [total - len(atrasados), len(atrasados)]
    barras = ax.bar(['No prazo', 'Atrasados'], valores, color=['#8a9b9d', '#C45136'])
    ax.bar_label(barras, labels=[brasileiro(v, 0) for v in valores], padding=4)
    ax.set_ylim(0, max(valores) * 1.15)
    ax.set_ylabel('Pedidos com prazo avaliável')
    ax.set_title(f'{brasileiro(len(atrasados) / total * 100)}% chegaram após o dia prometido')
    ax = eixos[0, 1]
    faixas = pd.cut(atrasados, [0, 7, 15, 30, float('inf')], labels=['1–7', '8–15', '16–30', 'Acima de 30']).value_counts(sort=False)
    barras = ax.bar(faixas.index.astype(str), faixas, color='#287D8E')
    ax.bar_label(barras, labels=[brasileiro(v, 0) for v in faixas], padding=4)
    ax.set_ylim(0, faixas.max() * 1.2)
    ax.set_xlabel('Dias após o dia prometido; extremos preservados')
    ax.set_ylabel('Pedidos atrasados')
    ax.set_title(f'Mediana: {brasileiro(atrasados.median(), 0)} dias; P90: {brasileiro(atrasados.quantile(.9), 0)} dias')
    for ax, coluna, titulo, unidade in [
        (eixos[1, 0], 'pedidos_atrasados', 'Quantidade por destino', 'Pedidos atrasados'),
        (eixos[1, 1], 'taxa_atraso', 'Taxa na mesma ordem de quantidade de atrasos', 'Atrasados / avaliáveis (%)'),
    ]:
        barras = ax.barh(estados.index, estados[coluna], color=['#C45136' if uf in ['SP', 'RJ', 'AL'] else '#8a9b9d' for uf in estados.index])
        ax.bar_label(barras, labels=[brasileiro(v, 0 if coluna == 'pedidos_atrasados' else 2) for v in estados[coluna]], padding=3, fontsize=8)
        ax.set_xlim(0, estados[coluna].max() * 1.3)
        ax.set_title(titulo)
        ax.set_xlabel(unidade)
        ax.set_ylabel('UF de destino; destaque SP, RJ, AL')
    eixos[1, 1].axvline(len(atrasados) / total * 100, color='#333', linestyle='--', label='Referência geral descritiva')
    eixos[1, 1].legend(loc='lower right', fontsize=8)
    fig.suptitle(f'Entregas: concentração e severidade • {brasileiro(total, 0)} pedidos avaliáveis', fontsize=16)
    contextualizar(fig, f"{pedidos_analisados['order_purchase_timestamp'].min():%m/%Y}–{pedidos_analisados['order_purchase_timestamp'].max():%m/%Y}")
    caminho = Path(__file__).resolve().parent.parent / 'web' / 'imagens' / 'grafico_entregas.png'
    caminho.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(caminho, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return caminho
