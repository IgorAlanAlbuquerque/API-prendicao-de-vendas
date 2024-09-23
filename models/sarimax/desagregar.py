from pandas import concat

def desagregar(historico_produto, ciclo):
    #ciclos equivalentes de periodos anteriores
    ciclos_equivalentes = [ciclo - j*100 for j in range(1, 3)]
        
    # Últimos 3 ciclos anteriores ao ciclo atual
    ciclos_anteriores = [ciclo - j for j in range(1, 4)]
        
    # Combina todos os ciclos relevantes
    ciclos_relevantes = ciclos_equivalentes + ciclos_anteriores
        
    # Filtra os ciclos relevantes no histórico
    historico_relevante = historico_produto[historico_produto['ano_ciclo'].isin(ciclos_relevantes)].copy()
        
    # Calcula a média da contribuição do produto nas vendas da loja nos ciclos anteriores
    if not historico_relevante.empty:
        # Pondera as vendas pela média do desconto
        historico_relevante.loc[:, 'ponderacao'] = historico_relevante['num_vendas_produto'] * (1 + historico_relevante['descontoMedio'])
        media_contribuicao = historico_relevante['ponderacao'].sum() / historico_relevante['num_vendas'].sum()
    else:
        media_contribuicao = 0
        
    return media_contribuicao


def desagregar_previsao(loja, vendas_agregadas, produtos, ciclo, previsao):
    divisoes = []
    for produto in produtos:
        # Filtra o histórico do produto específico
        historico_produto = loja[loja['cod_produto'] == produto].copy()

        # Renomeia a coluna 'num_vendas' para 'num_vendas_produto'
        historico_produto = historico_produto.rename(columns={'num_vendas': 'num_vendas_produto'})

        # Concatena o histórico do produto com as vendas agregadas
        historico_produto = concat([historico_produto.reset_index(drop=True), 
                                       vendas_agregadas['num_vendas'].reset_index(drop=True)], 
                                      axis=1)

        # Calcula a taxa de desagregação do produto para o ciclo específico
        produto_taxa = desagregar(historico_produto, ciclo)
        produto_taxa = float(produto_taxa)

        # Calcula a parte do produto na previsão total
        divisoes.append(produto_taxa)
        
    # Normalizar as divisões para que a soma seja igual a 1
    soma_divisoes = sum(divisoes)
    if soma_divisoes > 0:
        divisoes = [divisao / soma_divisoes for divisao in divisoes]
    else:
        divisoes = [0 for _ in divisoes]  # Se a soma for 0, todas as divisões serão 0

    divisoes = [taxa * previsao for taxa in divisoes]
    
    return divisoes