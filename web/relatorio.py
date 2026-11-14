"""Gera a página estática e tabelas de apoio a partir dos mesmos cálculos."""
from hashlib import sha256
from html import escape
from pathlib import Path

import pandas as pd

from analises import entregas as e, vendas as v, geo as g, vendedores as s
from analises import satisfacao_fidelizacao as f, pagamentos as p, avaliacoes as a
from graficos.formatacao import brasileiro as br

RAIZ = Path(__file__).resolve().parent.parent


def tabela(dados, titulo, arquivo, principal=False):
    dados = dados.to_frame() if isinstance(dados, pd.Series) else dados
    dados.to_csv(RAIZ / 'web' / 'tabelas' / f'{arquivo}.csv', encoding='utf-8-sig')
    exibicao = dados.head(12).reset_index().copy()
    for coluna in exibicao:
        if pd.api.types.is_numeric_dtype(exibicao[coluna]):
            casas = 2 if any(t in str(coluna) for t in ['taxa', 'participacao', 'valor', 'frete', 'ticket', 'media', 'mediana', 'dias', 'novembro', 'dezembro', 'diferenca', 'preco']) else 0
            exibicao[coluna] = exibicao[coluna].map(lambda x: 'Indisponível' if pd.isna(x) else br(x, casas) + ('%' if any(t in str(coluna) for t in ['taxa', 'participacao', 'percentual', 'cobertura']) else ''))
        else:
            exibicao[coluna] = exibicao[coluna].map(lambda x: nome(str(x)))
    exibicao.columns = [nome(str(c)) for c in exibicao.columns]
    html = exibicao.to_html(index=False, border=0, na_rep='Indisponível')
    if principal:
        return f'<h3>{escape(titulo)}</h3><div class="tabela" tabindex="0" role="region" aria-label="{escape(titulo)}">{html}</div><p><a href="tabelas/{arquivo}.csv" download>Baixar a seleção (CSV)</a></p>'
    return f'<details><summary>{escape(titulo)}</summary><p>Apoio técnico: primeiras 12 linhas da ordenação original; total {br(len(dados), 0)}. <a href="tabelas/{arquivo}.csv" download>Baixar todos os valores calculados (CSV)</a></p><div class="tabela" tabindex="0">{html}</div></details>'


def nome(texto):
    return {'cama_mesa_banho': 'Cama, mesa e banho', 'informatica_acessorios': 'Informática e acessórios', 'moveis_decoracao': 'Móveis e decoração', 'relogios_presentes': 'Relógios e presentes', 'customer_state': 'UF de destino', 'product_category_name': 'Categoria', 'mes_compra': 'Mês da compra', 'seller_id': 'ID do vendedor', 'payment_installments': 'Parcelas', 'diferenca_reais': 'Diferença (R$)', 'novembro': 'Novembro (R$)', 'dezembro': 'Dezembro (R$)', 'nota_media': 'Nota média', 'valor_produtos': 'Produtos (R$)', 'ticket_medio': 'Ticket (R$)', 'frete_medio_pedido': 'Frete médio (R$)'}.get(texto, texto.replace('_', ' ').capitalize())


def figura(arquivo, descricao):
    return f'<figure><a href="imagens/{arquivo}"><img src="imagens/{arquivo}" alt="{escape(descricao)}" loading="lazy"></a><figcaption>{escape(descricao)}</figcaption></figure>'


def descobertas():
    categorias = v.contribuicoes_categorias.head(3).copy()
    liquida = -v.contribuicoes_categorias['diferenca_reais'].sum()
    categorias['participacao_queda'] = -categorias['diferenca_reais'] / liquida * 100 if liquida > 0 else float('nan')
    reducoes = -categorias['diferenca_reais'].sum()
    comercial = f'Três categorias somam R$ {br(reducoes)} em reduções, equivalentes a {br(reducoes / liquida * 100)}% da queda líquida de R$ {br(liquida)}.' if liquida > 0 else f'A mudança líquida foi de R$ {br(-liquida)}; não se calcula participação em uma queda inexistente.'
    rj = e.episodio_rj
    qtd = rj['atrasados'].sum()
    base = rj['pedidos_avaliaveis'].sum()
    logistica = f'RJ: fevereiro e março de 2018 reuniram {br(qtd, 0)} atrasos em {br(base, 0)} pedidos avaliáveis ({br(qtd / base * 100)}%). O episódio aparece nos dois meses.'
    notas = f.resumo_momento.loc[True].loc[['Antes da entrega, após o dia prometido', 'Na entrega ou depois']]
    experiencia = f'Entre pedidos finalmente atrasados: nota {br(notas.iloc[0]["nota_media"])} durante a espera após o prazo ({br(notas.iloc[0]["pedidos"], 0)} pedidos), contra {br(notas.iloc[1]["nota_media"])} na entrega ou depois ({br(notas.iloc[1]["pedidos"], 0)} pedidos).'
    estados = g.resumo_integrado.nlargest(5, 'valor_produtos')[['participacao_vendas', 'pedidos_avaliaveis', 'taxa_atraso', 'ticket_medio', 'frete_medio_pedido', 'frete_percentual']].copy()
    taxa = e.quantidade_atrasados / e.total_analisado * 100
    frete = g.resumo_integrado['valor_frete'].sum() / v.total_vendido * 100
    acima = estados.index[(estados['taxa_atraso'] > taxa) | (estados['frete_percentual'] > frete)].tolist()
    estados.loc['Brasil'] = [100, e.total_analisado, taxa, v.total_vendido / len(v.pedidos_entregues), g.resumo_integrado['valor_frete'].sum() / len(v.pedidos_entregues), frete]
    parcelas = p.resumo_categoria_parcelas.loc[p.resumo_categoria_parcelas.index.get_level_values('payment_installments').isin([8, 10])].sort_values('valor_pago', ascending=False).head(1)
    categoria, vezes = parcelas.index[0]
    pag = parcelas.iloc[0]
    pagamento = f'{nome(categoria)}, {vezes} parcelas: {br(pag["pedidos"], 0)} pedidos, {br(pag["participacao_pedidos_categoria"])}% dos pedidos e {br(pag["participacao_valor_categoria"])}% do valor pago da categoria no complemento.'
    intervalos = e.resumo_intervalos_recortes
    etapas = intervalos.loc['RJ fev–mar/2018 atrasados'].iloc[:3]
    maior = etapas['mediana_dias'].idxmax()
    mensal = s.comparacao_celulas['pedidos_avaliaveis']
    trimestral = s.comparacao_trimestral_selecionada
    distribuicao = trimestral['pedidos_avaliaveis'].value_counts().sort_index().rename('celulas').to_frame()
    repeticao = trimestral.assign(acima=trimestral['taxa_atraso'] > trimestral['taxa_outros_vendedores']).reset_index().groupby('rotulo').agg(celulas=('acima', 'size'), acima_referencia=('acima', 'sum'), trimestres=('trimestre_compra', 'nunique'))
    return {
        'abertura': f'<p class="descoberta">{logistica}</p><p class="descoberta">{comercial}</p><p class="descoberta">{experiencia} São grupos distintos com sobreposição; não representa evolução da nota do mesmo cliente.</p>',
        'vendas': f'<p class="descoberta">{comercial}</p>' + tabela(categorias, 'Três maiores reduções, ordenadas pela diferença em reais; aumentos compensam parte da queda líquida', 'categorias_principais', True),
        'entregas': f'<p class="descoberta">{logistica}</p><p>Percentil 90: 90% dos atrasados tiveram atraso de até esse número de dias. Agosto/2018 é mês de borda; sua cobertura não comprova um mês completo.</p>' + tabela(rj, 'RJ lado a lado: mês da compra', 'rj_fevereiro_marco', True) + f'<p>Entre as três etapas dos atrasados do episódio, a maior mediana observada é em {maior}: {br(etapas.loc[maior, "mediana_dias"])} dias. Duração não identifica a causa do atraso. Medianas de etapas não devem ser somadas.</p>' + tabela(intervalos, 'Intervalos por recorte; grupos sobrepostos, sem soma entre grupos', 'intervalos_recortes'),
        'geografia': f'<p class="descoberta">Entre os cinco destinos de maior valor de produtos, {", ".join(acima)} combinam essa exposição com taxa de atraso ou proporção de frete acima da referência nacional.</p>' + tabela(estados, 'Seleção por valor dos produtos; Brasil calculado pelos totais', 'destinos_principais', True) + f'<p>Vendedores: {br((mensal == 1).sum(), 0)} de {br(len(mensal), 0)} células mensais têm um pedido ({br((mensal == 1).mean() * 100)}%). O complemento trimestral usa abril/2017–junho/2018 e dez vendedores selecionados por atrasos, com desempate por base e ID. Referência: demais vendedores da mesma UF/trimestre, sem o próprio vendedor.</p>' + tabela(trimestral, 'Complemento trimestral selecionado; contagens e pares completos no download', 'vendedores_trimestral') + tabela(distribuicao, 'Distribuição exata do tamanho das células selecionadas', 'bases_trimestrais') + tabela(repeticao, 'Repetição descritiva acima da referência; sem comprovação estatística', 'repeticao_vendedores') + '<p>A fragmentação e a seleção não sustentam ordenar o desempenho de forma estável; taxas isoladas não identificam os piores vendedores.</p>',
        'experiencia': f'<p class="descoberta">{experiencia}</p><p>Grupos diferentes, com pedidos presentes em mais de um recorte. A classificação usa datas registradas; não é comparação antes/depois do mesmo cliente.</p>' + tabela(notas, 'Notas de pedidos atrasados: dois momentos de resposta', 'notas_principais', True) + '<p>O detalhamento de severidade mantém a base de cada grupo; poucas avaliações após atrasos acima de 30 dias não sustentam generalização.</p>',
        'recompra': f'<p class="descoberta">{br(f.resumo_recompra["recompraram_90d"], 0)} de {br(f.resumo_recompra["elegiveis_90d"], 0)} clientes elegíveis retornaram em outro dia dentro de 90 dias: {br(f.resumo_recompra["taxa_90d"])}%.</p><p>Elegíveis têm 90 dias observáveis após a primeira compra entregue observada. Sem referência comparável, a taxa não é classificada como alta ou baixa.</p>',
        'pagamentos': f'<p class="descoberta">{pagamento}</p>' + tabela(parcelas, 'Maior grupo por valor pago entre oito/dez parcelas, categoria única', 'parcelamento_principal', True) + '<p>O valor pago pode incluir frete; a participação usa somente o complemento de cartão único e categoria única. Investigar quais produtos compõem essa concentração antes de propor intervenções.</p>',
    }


def gerar_relatorio():
    (RAIZ / 'web' / 'tabelas').mkdir(exist_ok=True)
    periodo = f"{v.itens_vendidos['order_purchase_timestamp'].min():%d/%m/%Y} a {v.itens_vendidos['order_purchase_timestamp'].max():%d/%m/%Y}"
    atraso = e.quantidade_atrasados / e.total_analisado * 100
    concentracao = e.resumo_estados.loc[['SP', 'RJ'], 'pedidos_atrasados'].sum() / e.quantidade_atrasados * 100
    delta = v.variacoes_nov_dez
    rc = f.resumo_recompra
    episodios = e.resumo_estado_mes.loc[['SP', 'RJ']].sort_values('atrasados', ascending=False).head(10)
    principal = episodios.iloc[0]
    destino, mes = episodios.index[0]
    queda = v.contribuicoes_categorias.head(3)
    oito_dez = p.resumo_categoria_parcelas.loc[p.resumo_categoria_parcelas.index.get_level_values('payment_installments').isin([8, 10])]
    destaques_cartao = oito_dez.sort_values('valor_pago', ascending=False).head(12)
    seccoes = []
    seccoes.append(f'''<section id="vendas"><p class="sobretitulo">01 / Contexto comercial</p><h2>Novembro → dezembro de 2017: menos pedidos e menor ticket</h2>
<p>O valor dos produtos variou <strong>{br(delta['valor_vendido'])}%</strong>, os pedidos {br(delta['quantidade_pedidos'])}% e o ticket {br(delta['ticket_medio'])}%. O valor vendido é a soma dos preços dos itens entregues, sem frete; não representa lucro ou receita própria da plataforma.</p>
{figura('grafico_vendas_mensais.png', 'Vendas, pedidos e ticket alinhados pelo mês da compra. Novembro e dezembro de 2017 estão destacados; meses de borda ficam fora da série comparável.')}
<p>As maiores contribuições negativas vieram de {', '.join(escape(c) for c in queda.index)}. A tabela mantém também os aumentos, que compensam parte das reduções. Pedidos com categorias diferentes aparecem em mais de uma categoria e não devem ser somados como exclusivos.</p>
{tabela(v.comparacao_nov_dez, 'Comparação e identidade do ticket: itens por pedido × preço médio por item', 'comparacao_nov_dez')}
{figura('grafico_contribuicoes.png', 'Diferenças por categoria entre novembro e dezembro de 2017, incluindo aumentos e saldo das demais categorias. Todas as contribuições estão na tabela.')}
{tabela(v.contribuicoes_categorias, 'Todas as contribuições por categoria (R$; dezembro menos novembro)', 'contribuicoes_categorias')}
{tabela(v.categorias_mensais, 'Categorias por mês: valores, itens e pedidos que contêm a categoria', 'categorias_mensais')}
{tabela(v.comparacao_anos, 'Contexto: fevereiro a julho de 2017 e 2018; poucos ciclos não demonstram sazonalidade', 'contexto_anos')}
<p><strong>Próximo passo:</strong> investigar disponibilidade e composição dos produtos nas categorias da queda. A variação observada não comprova mudança do preço do mesmo produto, campanha ou efeito de uma data comemorativa. Abril/julho permanece como exemplo didático nos documentos anteriores.</p></section>''')
    seccoes.append(f'''<section id="entregas"><p class="sobretitulo">02 / Frequência e severidade</p><h2>SP e RJ concentram {br(concentracao)}% dos atrasos</h2>
<p>São {br(e.quantidade_atrasados, 0)} atrasos entre {br(e.total_analisado, 0)} pedidos avaliáveis ({br(atraso)}%). O atraso compara o dia da entrega ao dia prometido. A mediana entre atrasados é {br(e.atrasos.median(), 0)} dias e o percentil 90 é {br(e.atrasos.quantile(.9), 0)} dias. Nenhum extremo foi removido.</p>
{figura('grafico_entregas.png', 'Volume e taxa usam a mesma ordem estadual, por quantidade de atrasos; SP, RJ e AL têm destaque. As faixas de duração incluem todos os extremos.')}
<p>O maior volume mensal entre SP/RJ está em <strong>{escape(destino)} / {mes}</strong>: {br(principal['atrasados'], 0)} atrasos em {br(principal['pedidos_avaliaveis'], 0)} entregas avaliáveis ({br(principal['taxa_atraso'])}%). O mês é sempre o da compra.</p>
{tabela(episodios, 'Dez episódios com mais atrasos em SP/RJ; taxa e exposição', 'episodios_sp_rj')}
{tabela(e.concentracao_mensal, 'Concentração SP/RJ em cada mês: episódios e persistência', 'concentracao_mensal')}
{tabela(e.resumo_estado_mes, 'Todos os destinos e meses; duração ausente quando não há atraso', 'estado_mes')}
{tabela(e.resumo_faixas, 'Severidade: faixas exclusivas e participação nos atrasos', 'faixas_atraso')}
{tabela(f.resumo_notas_faixas, 'Notas por severidade e momento da resposta; média por pedido dentro do recorte', 'notas_faixas')}
{tabela(e.resumo_intervalos, 'Intervalos logísticos (dias); ausências e sequências negativas separadas', 'intervalos')}
<p><strong>Investigação:</strong> examinar a sequência compra → aprovação → transportador → cliente nos episódios acima e nos casos com mais de 30 dias. Os intervalos não identificam isoladamente um responsável; custo, transportadora e viabilidade ainda precisam ser apurados.</p></section>''')
    seccoes.append(f'''<section id="geografia"><p class="sobretitulo">03 / Exposição comercial e logística</p><h2>Volume, ticket e frete precisam ser lidos juntos</h2>
<p>Vendas incluem {br(len(v.pedidos_entregues), 0)} pedidos entregues; prazos usam {br(e.total_analisado, 0)} com datas válidas. Os oito pedidos sem prazo avaliável permanecem no total comercial. Frete é o valor registrado nos itens, sem evidência de custo logístico da empresa.</p>
{figura('grafico_geografia.png', 'Participação nas vendas, ticket e frete nos destinos principais. A tabela inclui todas as UFs e os denominadores comerciais e logísticos.')}
{tabela(g.resumo_integrado.sort_values('valor_produtos', ascending=False), 'Todas as UFs: vendas, frete, ticket, atrasos e exposição', 'geografia')}
<p><strong>Próximo passo:</strong> confrontar destinos de maior volume com taxa de atraso e proporção de frete antes de priorizar uma investigação. Um cliente pode aparecer em mais de um estado; a soma estadual de clientes não equivale necessariamente ao total nacional distinto.</p>
<h3>Vendedores: associação ao atraso, com contexto de destino e período</h3>
{figura('grafico_vendedores.png', 'Dez vendedores com mais pedidos associados a atrasos, com taxa e quantidade avaliável. Referência nacional descritiva, sem ajuste de composição.')}
<p>O recorte complementar com vendedor único exclui {br(s.pedidos_excluidos_multivendedor, 0)} pedidos multivendedor. As células vendedor × destino × mês mantêm bases pequenas visíveis. Não há ranking ajustado: composição de produtos, operação e responsabilidade não foram controladas.</p>
{tabela(s.resumo_vendedores, 'Correspondência dos rótulos aos IDs completos; todos os vendedores', 'vendedores')}
{tabela(s.comparacao_celulas, 'Comparações por destino e mês: vendedor único e referência da mesma célula', 'vendedores_celulas')}
{tabela(s.ranking_vendedores.head(10), 'Exemplos de taxas elevadas com bases pequenas: não são prioridade automática', 'vendedores_bases_pequenas')}
<p><strong>Próximo passo:</strong> comparar os vendedores de maior volume dentro do mesmo destino/mês e verificar se os padrões persistem. A entrega final de um pedido multivendedor não revela quem causou seu atraso.</p></section>''')
    seccoes.append(f'''<section id="experiencia"><p class="sobretitulo">04 / Experiência registrada</p><h2>Avaliações durante a espera e após o recebimento têm significados diferentes</h2>
<p>A comparação histórica é {br(f.resumo_satisfacao.loc[False, 'nota_media'])} no prazo versus {br(f.resumo_satisfacao.loc[True, 'nota_media'])} atrasados, com uma nota média por pedido. Entre registros associados a atrasados, {br(f.percentual_respostas_antes_atrasados)}% foram respondidos antes da entrega registrada. Esse percentual usa registros, não pedidos.</p>
{figura('grafico_satisfacao_fidelizacao.png', 'Notas por situação final da entrega e momento da resposta, com quantidade de pedidos por grupo. Associação observada, sem demonstração causal.')}
{tabela(f.resumo_satisfacao, 'Comparação histórica: cobertura e média por pedido', 'satisfacao_historica')}
{tabela(f.resumo_momento, 'Momentos da resposta: registros, pedidos e médias', 'momento_avaliacoes')}
{tabela(pd.Series({'criacao_ausente': a.qualidade_datas['review_creation_date'], 'resposta_ausente': a.qualidade_datas['review_answer_timestamp'], 'resposta_antes_criacao': a.respostas_antes_criacao}), 'Qualidade das datas de avaliação na base completa', 'qualidade_avaliacoes')}
<p>Na base completa, {br(f.pedidos_multiplas_avaliacoes, 0)} pedidos têm várias avaliações; no recorte de prazo, {br(f.pedidos_multiplos_recortes, 0)} aparecem em mais de um recorte temporal. A nota é consolidada por pedido dentro de cada recorte. A soma dos pedidos dos grupos pode exceder o total distinto. Registros não classificáveis são preservados.</p>
<p><strong>Próximo passo:</strong> examinar avaliações de atrasos severos, distinguindo resposta durante a espera de resposta posterior. A situação final não comprova que o cliente já conhecia o desfecho quando respondeu.</p></section>''')
    seccoes.append(f'''<section id="recompra"><p class="sobretitulo">05 / Comportamento de compra</p><h2>Múltiplos pedidos e recompra observável são indicadores diferentes</h2>
<p>{br(rc['multiplos_pedidos'], 0)} clientes fizeram múltiplos pedidos entregues; {br(rc['outro_dia'], 0)} compraram em dias diferentes. Entre os primeiros, {br(rc['multiplos_pedidos'] - rc['outro_dia'], 0)} concentraram todas as compras no mesmo dia.</p>
{figura('grafico_recompra.png', 'Compras em dias diferentes são separadas de múltiplos pedidos. A taxa de 90 dias usa apenas clientes com janela completa; não mede lealdade.')}
<p>Até o corte observado em {f.data_corte_recompra:%d/%m/%Y}, {br(rc['elegiveis_90d'], 0)} clientes tinham 90 dias de observação desde a primeira compra. {br(rc['recompraram_90d'], 0)} voltaram em outro dia dentro de 1–90 dias: <strong>{br(rc['taxa_90d'])}%</strong>. Não se exige que a primeira entrega tenha ocorrido antes da segunda compra.</p>
{tabela(rc, 'Populações da recompra observada', 'recompra')}
{tabela(f.resumo_recorrencia, 'Referência histórica de múltiplos pedidos: clientes, pedidos e valores', 'multiplos_pedidos')}
<p><strong>Limite e próximo passo:</strong> o status final delivered e a cobertura desigual podem afetar a leitura; a última data não comprova extração completa. Investigar coortes com acompanhamento completo antes de definir ações de retenção. Nenhuma relação entre atraso e recompra foi estimada.</p></section>''')
    seccoes.append(f'''<section id="pagamentos"><p class="sobretitulo">06 / Pagamentos</p><h2>Parcelamento: quantidade e mediana dão contexto às médias</h2>
<p>O recorte inclui {br(len(p.compras_cartao), 0)} pedidos com pagamento único no cartão, parcelas ≥ 1 e valor positivo. Acima de dez parcelas: {br(p.parcelas_raras['quantidade_pedidos'].sum(), 0)} pedidos ({br(p.parcelas_raras['participacao_pedidos'].sum())}%).</p>
{figura('grafico_pagamentos.png', 'Média e mediana em pontos, com volume alinhado entre uma e dez parcelas. Grupos acima de dez estão disponíveis na tabela, sem destaque desproporcional.')}
{tabela(p.resumo_formas, 'Formas de pagamento: registros, pedidos e participação no valor', 'formas_pagamento')}
{tabela(p.resumo_parcelamento, 'Todas as quantidades de parcelas, incluindo grupos raros', 'parcelamento')}
<p>A comparação por categoria cobre {br(len(p.cartao_categoria), 0)} pedidos ({br(len(p.cartao_categoria) / len(p.compras_cartao) * 100)}% do recorte); exclui {br(p.excluidos_multicategoria, 0)} multicategoria. Cada pedido contribui uma vez com seu pagamento integral. Não há rateio arbitrário.</p>
{tabela(destaques_cartao, 'Oito e dez parcelas: maiores volumes de valor pago por categoria, com quantidade e participação', 'destaques_oito_dez')}
{tabela(p.resumo_categoria_parcelas, 'Todas as categorias e parcelas; quantidade, média, mediana e participação', 'categoria_parcelas')}
<p><strong>Próximo passo:</strong> avaliar a representatividade de oito e dez parcelas dentro de cada categoria. Maior valor médio é associação observada; não comprova que oferecer mais parcelas aumentará vendas, margem ou conversão.</p></section>''')
    seccoes.append(f'''<section id="prioridades"><h2>Três investigações antes de uma decisão operacional</h2><ol>
<li><strong>Logística:</strong> começar por {escape(destino)} / {mes} e demais episódios de SP/RJ; confrontar volume, taxa e intervalos dos atrasos severos para localizar onde a espera se acumula.</li>
<li><strong>Comercial:</strong> investigar produtos e disponibilidade em {', '.join(escape(c) for c in queda.index)} na mudança novembro/dezembro de 2017, preservando categorias que cresceram.</li>
<li><strong>Experiência:</strong> examinar notas durante a espera e após a entrega nos atrasos acima de 30 dias; buscar evidência sobre a jornada antes de formular intervenções.</li></ol>
<p>São prioridades de investigação histórica. Responsabilidade, viabilidade e custo ainda precisam ser apurados. Não há previsão, cenário simulado ou evidência de efeito causal.</p></section>''')
    html = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Olist: vendas, entregas e experiência do cliente</title><link rel="stylesheet" href="style.css"></head><body>
<a class="pular" href="#conteudo">Pular para o conteúdo</a><header><p class="sobretitulo">Projeto Olist / Análise histórica</p><h1>Vendas, entregas e experiência do cliente</h1><p>Objetivo: localizar mudanças comerciais e grupos com atrasos para orientar investigações, sem atribuir causas que a base não permite demonstrar.</p><p>Compras entregues: {periodo}. Fonte: CSVs locais Olist. Resultados descrevem essa extração histórica.</p>
<div class="indicadores"><p><strong>{br(v.total_vendido)} reais</strong>produtos; sem frete</p><p><strong>{br(concentracao)}%</strong>dos atrasos em SP e RJ</p><p><strong>{br(delta['valor_vendido'])}%</strong>vendas: nov → dez/2017</p></div>
<p>Descobertas prioritárias: SP/RJ concentram volume de atrasos; novembro/dezembro combina menos pedidos e menor ticket; {br(f.percentual_respostas_antes_atrasados)}% das respostas de pedidos atrasados antecedem a entrega.</p></header>
<nav aria-label="Temas">{''.join(f'<a href="#{i}">{nome}</a>' for i, nome in [('vendas','Vendas'),('entregas','Entregas'),('geografia','Destinos e vendedores'),('experiencia','Avaliações'),('recompra','Recompra'),('pagamentos','Pagamentos'),('prioridades','Prioridades')])}</nav>
<main id="conteudo">{''.join(seccoes)}</main><footer><p>Os critérios variam por tema: prazo exige datas válidas; vendas incluem todos os entregues; cartão e recompra têm recortes próprios. Valores exportados preservam a precisão calculada; a exibição usa formato brasileiro.</p><p><a href="../Estrutura_de_pensamento/Critérios dos indicadores.md">Critérios e rastreabilidade</a> · <a href="../Estrutura_de_pensamento/Entrega da evolução.md">Registro da entrega</a></p></footer></body></html>'''
    caminho = RAIZ / 'web' / 'index.html'
    sinteses = descobertas()
    for tema in ['vendas', 'entregas', 'geografia', 'experiencia', 'recompra', 'pagamentos']:
        inicio = html.index(f'<section id="{tema}">')
        posicao = html.index('</h2>', inicio) + len('</h2>')
        html = html[:posicao] + sinteses[tema] + html[posicao:]
    inicio = html.index('<div class="indicadores">')
    fim = html.index('</header>', inicio)
    html = html[:inicio] + sinteses['abertura'] + html[fim:]
    html = html.replace('primeira compra.', 'primeira compra entregue observada.')
    html = html.replace(', '.join(escape(c) for c in queda.index), ', '.join(escape(nome(c)) for c in queda.index))
    html = html.replace('avaliar a representatividade de oito e dez parcelas dentro de cada categoria.', 'investigar os produtos que compõem a concentração de oito e dez parcelas já identificada.')
    html = html.replace(f'começar por {escape(destino)} / {mes} e demais episódios de SP/RJ;', 'começar pelo RJ em fevereiro/março de 2018; obter registros de transporte e ocorrências para explicar diferenças de espera e apoiar a revisão do processo;')
    caminho.write_text(html, encoding='utf-8')
    registrar_base(periodo)
    return caminho


def registrar_base(periodo):
    linhas = []
    for caminho in sorted((RAIZ / 'dados' / 'olist').glob('*.csv')):
        df = pd.read_csv(caminho)
        datas = []
        for coluna in df.columns:
            if coluna.endswith(('_date', '_timestamp', '_at')) or coluna == 'shipping_limit_date':
                valores = pd.to_datetime(df[coluna], errors='raise').dropna()
                datas.append(f'{coluna}: {valores.min()} a {valores.max()}; ausentes={df[coluna].isna().sum()}')
        linhas.append({'arquivo': caminho.name, 'sha256': sha256(caminho.read_bytes()).hexdigest(), 'linhas': len(df), 'datas_observadas': '; '.join(datas)})
    pd.DataFrame(linhas).to_csv(RAIZ / 'web' / 'tabelas' / 'versao_base.csv', index=False, encoding='utf-8-sig')
    referencia = pd.Series({'pedidos_entregues': len(v.pedidos_entregues), 'itens': len(v.itens_vendidos),
                           'valor_produtos': v.total_vendido, 'pedidos_avaliaveis': e.total_analisado,
                           'atrasados': e.quantidade_atrasados, 'respostas_anteriores_atrasados_pct': f.percentual_respostas_antes_atrasados})
    referencia.to_csv(RAIZ / 'web' / 'tabelas' / 'referencia.csv', encoding='utf-8-sig')
