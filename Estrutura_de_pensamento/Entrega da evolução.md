# Registro da evolução Olist

## Escopo e decisões

Na primeira evolução, o pedido de implementação substituiu o papel de mentoria do plano. O registro daquela execução indicou a branch `codex/evolucao-olist`, preservando a alteração prévia de `.gitignore`. Sem publicação ou alteração dos CSVs. A pedido do usuário, a execução dos testes restantes foi reservada à última etapa.

| Etapa | Entrega |
|---|---|
| 0 | Critérios comuns, perguntas gerenciais, manifesto SHA-256, intervalos e totais de referência |
| 1 | Múltiplos pedidos, compras em dias diferentes, primeira compra posterior e elegibilidade de 90 dias |
| 2 | Momento da resposta, consolidação por pedido/recorte, cobertura e sobreposição |
| 3 | Estado/mês, concentração mensal SP/RJ, faixas, P90, notas por severidade e intervalos logísticos |
| 4 | Variações nov/dez, contribuições positivas e negativas, categoria ausente com zero e identidade do ticket |
| 5 | Geografia integrada, vendedor único, comparação destino/mês e rótulos rastreáveis |
| 6 | Parcelas raras, categorias únicas, cobertura, quantidade, média e mediana |
| 7 | Seis geradores revistos; satisfação/recompra separadas; figura de contribuições |
| 8 | Objetivo geral, navegação temática, evidências, limites e três prioridades |
| 9 | Concluída por decisão de não incluir mapa: a pergunta é comparar destinos/períodos e volume/taxa; tabelas e barras já respondem sem geometria adicional |
| 10 | Regeneração integrada, quatro testes aprovados e página conferida manualmente pelo usuário |

## Escolha visual e integridade

Perguntas: comparação de volume/taxa, evolução temporal, composição da queda, contexto de notas e recompra. Barras têm origem zero, figuras temporais usam meses alinhados, contribuições mostram ambos os sinais. Pontos de pagamentos não sugerem continuidade. Recorrência fica em figura própria para evitar sugerir relação não analisada com atraso. Fonte e recorte acompanham as figuras; tabelas constituem alternativa textual e têm acesso por teclado.

Narrativa: contexto comercial → concentração/severidade → experiência → investigações. Pagamentos e recompra são blocos próprios. A dimensão territorial não é necessária para a comparação exata das UFs; um mapa não foi acrescentado apenas por estética. Nenhuma dependência nova foi instalada.

O relatório estático é regenerado dos cálculos em `web/relatorio.py`, reduzindo o risco dos números escritos manualmente. As tabelas exportadas preservam precisão e denominadores; os documentos anteriores ficam como histórico didático, com aviso para consultar os critérios vigentes.

## Avaliação da entrega (escala 1–5)

- Esclarecimento dos dados: 4/5. Populações, períodos, cardinalidades e coberturas estão explícitos; completude e semântica operacional da extração não são comprovadas.
- Qualidade da história: 4/5. Abertura e três prioridades integram as descobertas; causas e decisões operacionais ainda exigem dados externos.
- Uso dos indicadores: 4/5. Volume acompanha taxa, média acompanha mediana/quantidade; pequenas células e viés de seleção permanecem visíveis.

As notas acima são autoavaliação qualitativa da entrega. As notas numéricas da revisão inicial não constam do plano, portanto não foi calculada melhora de pontuação.

## Comandos registrados na primeira evolução

```powershell
.\venv\Scripts\python.exe main.py --sem-abrir
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

O comando de testes acima registra a primeira evolução; a pasta `tests/` não está presente na versão local conferida nesta revisão documental. Não representa instrução reproduzível da versão atual.

Para regenerar a entrega atual, executar `main.py --sem-abrir` da raiz com as dependências instaladas. Sem `--sem-abrir`, o script também abre o navegador. A geração sobrescreve saídas derivadas em `web/`, preservando os dados de origem. A revisão documental não executou essa geração.

## Limitações remanescentes

Dados históricos; cobertura desigual; notas com sobreposição; recortes de categoria/vendedor únicos são seleções; células pequenas não sustentam comparação estável. Não foram estimadas causalidade, rentabilidade, responsabilidade logística ou efeito de prazo sobre recompra. A página oferece síntese e detalhamento; arquivos CSV grandes devem ser explorados fora do navegador quando necessário.

## Encerramento e evidências de validação

- A execução de `main.py --sem-abrir` concluiu a geração de oito figuras, tabelas e página.
- A execução final de `python -m unittest discover -s tests -v` aprovou quatro testes: recompra com limites de datas, momento das avaliações, categorias ausentes em um mês e reconciliações dos cruzamentos.
- Os totais recalculados preservaram a referência: 96.478 pedidos entregues, 110.197 itens, R$ 13.221.498,11 em produtos, 96.470 pedidos com prazo avaliável e 6.534 atrasados.
- O usuário confirmou: “A página está correta, verifiquei manualmente”. A apresentação foi aceita com base nessa conferência.
- A ferramenta de navegação interrompeu a inspeção por não conseguir identificar a URL com segurança. A conferência visual é do usuário; não há registro das larguras específicas utilizadas, portanto não se afirma teste automatizado em 1440, 768 e 390 pixels.

A implementação foi entregue localmente e a apresentação foi aceita pelo usuário. A etapa opcional de mapa foi encerrada sem inclusão, conforme a justificativa acima. Não houve commit, publicação ou deploy nesta entrega.

## Segunda evolução: clareza das descobertas

Contrato de leitura por bloco: pergunta de gestão → descoberta calculada → números essenciais → evidência curta → significado → investigação seguinte. Vendas, notas, recompra e pagamentos reutilizam dados já calculados; intervalos segmentados do RJ e comparação trimestral exigiram novos recortes.

RJ fevereiro/março de 2018 usa taxa conjunta pelas contagens somadas. Intervalos preservam timestamps, separam pares ausentes e negativos, incluem prazo prometido e tempo total real; recortes se sobrepõem e medianas não se somam. Os resultados estão em web/tabelas/intervalos_recortes.csv.

Vendedores: vendedor único, abril/2017–junho/2018, dez vendedores selecionados por quantidade de atrasos, desempate por base e ID; referência da mesma UF/trimestre exclui o próprio vendedor. Sem pares, taxa indisponível. Distribuição de bases e repetição acima da referência são descritivas, sem comprovar estabilidade de desempenho.

Vendas: três menores diferenças monetárias, participação conjunta sobre a queda líquida, mantendo aumentos compensatórios. Sem queda positiva, participação indisponível. Geografia: cinco estados por valor de produtos e referência nacional calculada pelos totais. Pagamentos: maior valor pago entre oito/dez parcelas, dentro de cartão único/categoria única; pagamento pode incluir frete.

Abertura e tabelas principais tornam explícitas as descobertas; prévias técnicas limitadas a 12 linhas são apoio e downloads completos preservam os dados. A recompra de 90 dias é indicador textual, com numerador, elegibilidade e primeira compra entregue observada. Notas de espera e entrega/depois são grupos distintos com sobreposição.

Testes dispensados por solicitação do usuário nesta segunda evolução. A geração integrada utiliza as validações existentes dos módulos. A aprovação visual anterior refere-se à primeira versão; a nova versão ainda precisa de observação em 1440, 768 e 390 pixels e leitura orientada pelo usuário. Etapas 0–8 implementadas; etapa 9 com testes dispensados e conferência visual/compreensão pendentes. Sem publicação ou deploy.

Autoavaliação editorial: dados 4/5, história 4/5, indicadores 4/5, pelas seleções explícitas, três descobertas calculadas e referências contextualizadas. Sem conferência visual nova, não se afirma melhora garantida das notas anteriores.

## Revisão documental final — 14/11/2026

Após decidir manter a versão atual do projeto, o usuário solicitou a revisão de todos os dez Markdown de `Estrutura_de_pensamento`. Foram complementados contexto, fontes, população, lógica, indicadores, descobertas, contribuição gerencial, limitações e rastreabilidade, conforme a necessidade de cada arquivo. A lógica didática inicial foi preservada e as extensões foram incorporadas aos documentos correspondentes.

Pagamentos e satisfação/recompra receberam documentação mais completa. Vendas passou a explicar a contribuição das categorias; entregas, o episódio e seus intervalos; geografia, os denominadores e a referência nacional; vendedores, os complementos mensal/trimestral e a seleção. Perguntas foi organizado por tema, e Critérios deixou de repetir o histórico de execução. O DER teve o caminho corrigido e as checagens de chaves explicitadas.

As conferências desta revisão foram de documentação, leitura dos módulos e comparação com fontes/CSVs derivados, incluindo checagens diretas de chaves e relacionamentos. Não houve alteração de Python, CSV, HTML, figuras ou README, nem execução de suíte de testes, regeneração da entrega, commit, publicação ou deploy por esta tarefa.

Continuam registradas as limitações de apresentação: taxa de recompra arredondada como “1” na tabela de apoio, embora texto e CSV mantenham 1,30%; sobreposições de anotações; repetição de trechos; e falta de validação da versão final em larguras específicas. A confirmação visual da primeira entrega não deve ser estendida automaticamente à segunda.

Os próximos passos dos documentos são possibilidades de investigação, sem reabrir a implementação encerrada. O código e os CSVs continuam sendo a referência para recálculo se houver nova extração.
