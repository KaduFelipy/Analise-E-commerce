from matplotlib.ticker import FuncFormatter


def brasileiro(valor, casas=2):
    return f'{valor:,.{casas}f}'.replace(',', '_').replace('.', ',').replace('_', '.')


def contextualizar(fig, periodo):
    for ax in fig.axes:
        for eixo in (ax.xaxis, ax.yaxis):
            if not eixo.get_units():
                eixo.set_major_formatter(FuncFormatter(lambda v, p: brasileiro(v, 0 if v == int(v) else 2)))
    fig.supxlabel(f'Fonte: Olist • compra: {periodo} • base histórica; associação não implica causa', fontsize=9)
