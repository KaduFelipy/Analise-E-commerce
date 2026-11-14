# Critérios dos indicadores

Público: gestão comercial, logística e experiência do cliente. Uso: selecionar investigações históricas; a base não mede margem, conversão de visitas ou responsabilidade operacional.

## Fonte, versão e período

Os CSVs originais em `dados/olist/` são somente leitura. `web/tabelas/versao_base.csv` identifica cada arquivo pelo SHA-256, quantidade de linhas e intervalo observado de cada campo de data. Esse manifesto identifica a extração local; não afirma uma versão editorial ou data de extração desconhecida.

`web/tabelas/referencia.csv` registra os totais recalculados. Referência anterior: 96.478 pedidos entregues, 110.197 itens, R$ 13.221.498,11 em produtos; 96.470 pedidos com prazo avaliável e 6.534 atrasados. Os oito pedidos entregues sem data necessária para prazo entram nas vendas e ficam fora da avaliação logística.

As tabelas de apoio mantêm os valores calculados sem arredondamento prévio. A página e os gráficos formatam números para leitura, com as limitações conhecidas registradas abaixo. Os dados de origem permanecem intactos. A representação monetária segue o pandas existente; as reconciliações de vendas usam `math.isclose`, com `rel_tol=1e-9` e/ou `abs_tol=0.01` conforme a chamada. Há tolerância numérica, não garantia de exatidão contábil ao centavo.

## Perguntas, populações e denominadores

| Tipo e pergunta | Decisão apoiada / público | População e unidade | Período e fórmula | Limite |
|---|---|---|---|---|
| Descrição: quanto foi vendido? | Dimensionar exposição / comercial | Todos os pedidos delivered; preços e fretes somados por item | Compra observada; valor = soma price; ticket = valor / pedidos distintos | Valor de produtos não é lucro nem receita própria |
| Comparação: o que compõe a queda nov/dez? | Selecionar categorias a investigar / comercial | Itens de pedidos delivered; Sem categoria preservada | Nov/dez 2017; diferença dezembro − novembro por categoria, inclusive ausências com zero | Pedidos multicategoria não são exclusivos; preço médio reflete mix |
| Descrição: onde e quando há atrasos? | Selecionar episódios / logística | Delivered com entrega e promessa preenchidas; uma linha/pedido | Mês da compra; atraso = dia real > dia prometido; taxa = atrasados / avaliáveis | Destino não identifica responsabilidade |
| Comparação: qual a severidade? | Investigar esperas longas / logística | Somente pedidos atrasados | Dias inteiros entre datas normalizadas; mediana, P90 e faixas 1–7, 8–15, 16–30, >30 | Sem exclusão de extremos; grupos sem atrasos não recebem duração zero |
| Investigação: onde se acumula a espera? | Selecionar etapas a examinar / logística | Pedidos com prazo avaliável; pares de datas válidos não negativos | Compra→aprovação→transportador→cliente; duração real em dias fracionários | Cada par tem cobertura própria; não comprova culpado |
| Comparação: vendedores em contexto semelhante? | Selecionar pedidos a investigar / logística | Associações históricas; complementos de vendedor único | Mensal por UF; trimestral abril/2017–junho/2018, dez vendedores por atrasos | Referência mensal inclui o próprio; trimestral exclui; sem ranking ajustado ou prova de responsabilidade |
| Comparação: notas variam por situação e momento? | Separar espera e recebimento / experiência | Registros associados a pedidos com prazo; média de notas por pedido dentro do recorte | Situação final e resposta anterior à entrega ou na entrega/depois; anterior separada pelo dia prometido | Pedido pode estar em vários grupos; associação sem causa |
| Descrição: quantos fizeram múltiplos pedidos? | Descrever base / comercial | Cliente unique com pedidos entregues | Dois ou mais pedidos; cobertura histórica inteira | Compras no mesmo dia não demonstram retorno |
| Comparação: quantos retornaram em 90 dias? | Definir investigação de coortes / experiência | Clientes cuja primeira compra entregue observada tem janela de 90 dias até o corte | Segunda data distinta; diferença entre dias de compra 1–90 inclusive; taxa / clientes elegíveis | Não exige primeira entrega antes da segunda compra; status final e cobertura desigual limitam leitura |
| Comparação: parcelamento varia por categoria? | Examinar composição de pagamentos / comercial | Pagamento único no cartão, parcelas ≥1 e valor positivo; categoria única no complemento | Quantidade, participação, média e mediana por parcelas; categoria única contém Sem categoria | Exclui multicategoria; não rateia valor pago; não comprova benefício de mais parcelas |

## Regras de junção e decomposição

Pedidos, clientes e produtos exigem cardinalidade declarada nas junções. Avaliações são consolidadas por pedido antes da média do grupo. Estados comerciais somam itens; prazos estaduais agregam pedidos antes da junção. Pedidos multivendedor permanecem nas associações e são excluídos somente do complemento de vendedor único. Soma de associações não é total nacional de pedidos.

Identidades: valor = pedidos × ticket; ticket = itens por pedido × preço médio por item. Diferenças monetárias por categoria somam a diferença nacional. Aumentos compensatórios são preservados. Comparar fevereiro–julho entre anos é contexto descritivo, sem afirmar sazonalidade.

`review_creation_date` e `review_answer_timestamp` são tratados como criação e resposta registradas. Não se assume que criação seja entrega nem que resposta prove recebimento. Tipos, ausências e respostas anteriores à criação são relatados; a semântica operacional não foi confirmada por documentação adicional à extração. Para espera após prazo usa-se o dia normalizado; para resposta anterior ao recebimento compara-se o timestamp integral. “Na entrega ou depois” inclui igualdade de timestamps. Não classificáveis são preservados.

O corte da recompra é a última data de compra entre pedidos entregues observados. Presença de registros até esse dia não comprova completude da extração. As taxas históricas de múltiplos pedidos e de recompra em 90 dias têm denominadores diferentes.

## Prioridades e limites

1. Concentração dos atrasos por destino, mês e severidade.
2. Composição da mudança comercial novembro/dezembro de 2017.
3. Momento da resposta nas avaliações dos atrasos severos.

As relações métricas acima são contábeis/descritivas. Não foi definido indicador antecedente causal, meta operacional, previsão ou experimento. Custos e viabilidade de intervenções não estão disponíveis.

## Recortes específicos da versão final

- **Vendas:** comparar novembro/dezembro de 2017 e preservar todas as categorias. A participação das três maiores reduções divide sua soma pela queda líquida nacional, com aumentos compensatórios mantidos. Se não há queda positiva, essa participação não é calculada.
- **Entregas:** o episódio do RJ usa compras de fevereiro/março de 2018. Somar numeradores e denominadores antes da taxa conjunta. Intervalos separam recortes gerais, no prazo, atrasados e acima de 30 dias; estes últimos se sobrepõem. Pares ausentes e negativos ficam fora da duração daquele intervalo, com contagens preservadas.
- **Geografia:** selecionar cinco estados pelo valor dos produtos e mostrar referência nacional calculada pelos totais. Oito pedidos sem prazo avaliável continuam no denominador comercial.
- **Vendedores:** selecionar vendedor único e compras de abril/2017–junho/2018; escolher dez vendedores por atrasos, com desempate por base e ID. Subtrair os pedidos/atrasos do próprio vendedor da referência UF/trimestre. Sem outros pedidos, a taxa dos demais é indisponível. Repetição acima da referência conta células, não efeitos persistentes comprovados.
- **Avaliações:** consolidar por pedido dentro de cada recorte. Quantidade de registros, quantidade de pedidos e cobertura da situação têm denominadores distintos. Não somar grupos sobrepostos como se fossem exclusivos.
- **Recompra:** corte em 29/08/2018, primeira compra entregue observada e nova data distinta em 1–90 dias. Os 75.387 elegíveis e os 93.358 clientes históricos são populações diferentes.
- **Pagamentos:** maior grupo por valor pago entre oito/dez parcelas no complemento de cartão único e categoria única. O total pode incluir frete; participações da categoria não representam toda a base comercial.

## Do cálculo à apresentação

`analises/` produz os resultados; `graficos/` gera oito figuras; `web/relatorio.py` organiza descobertas, tabelas e HTML. As funções analíticas próprias são `calcular_contribuicoes`, `classificar_momento` e `calcular_recompra`; outros indicadores são construídos por filtros, junções e agregações nos módulos.

Os CSVs derivados preservam precisão; arredondamento deve servir somente à leitura. Na versão atual, a tabela de apoio da recompra no HTML mostra a taxa como “1”; o texto principal (1,30%) e o CSV mantêm a interpretação correta. A documentação registra essa limitação sem mudar o código ou as saídas.

As prévias técnicas do HTML têm limite de 12 linhas e não substituem o arquivo completo. Em intervalos sobrepostos ou tabelas grandes, consultar também o CSV para conferir a evidência usada. Medianas de etapas não são somadas.

## Navegação e registro de validação

- [Perguntas e decisões apoiadas](Perguntas.md).
- [Modelo de relações e checagens das chaves](Diagrama%20de%20rela%C3%A7%C3%A3o%20das%20tabelas.md).
- [Registro das evoluções, verificações anteriores e pendências](Entrega%20da%20evolu%C3%A7%C3%A3o.md).
- [Manifesto da base](../web/tabelas/versao_base.csv) e [referência dos totais](../web/tabelas/referencia.csv).

Resultados documentados descrevem a versão local conferida; uma nova base exige recálculo. Histórico de testes, aprovação visual e autoavaliações fica no registro da evolução, não constitui nova execução de validação nesta revisão documental.
