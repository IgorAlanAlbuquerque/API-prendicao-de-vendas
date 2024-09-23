from pandas import DataFrame

def agregar(loja):
    # Agregação do número de vendas por ciclo
    total_vendas_loja_ciclo = loja.groupby(['cod_loja', 'ano_ciclo']).agg({'num_vendas': 'sum'}).reset_index()
    total_vendas_loja_ciclo = total_vendas_loja_ciclo.rename(columns={'num_vendas': 'total_vendas'})

    # Mesclando o total de vendas com o dataframe original
    loja = loja.merge(total_vendas_loja_ciclo, on=['cod_loja', 'ano_ciclo'])

    loja['peso'] = loja['num_vendas'] / loja['total_vendas']

    # Calculando o desconto médio ponderado para cada loja e ciclo
    desconto_medio_ponderado = loja.groupby(['cod_loja', 'ano_ciclo']).apply(
        lambda x: (x['descontoMedio'] * x['peso']).sum() / x['peso'].sum()
    ).reset_index(drop=True)

    # Mesclando o desconto médio ponderado com as vendas agregadas
    vendas_agregadas = loja.groupby(['cod_loja', 'ano_ciclo']).agg({'num_vendas': 'sum'}).reset_index()
    # Adiciona a coluna 'descontoMedio_ponderado' ao DataFrame final
    vendas_agregadas['descontoMedio_ponderado'] = desconto_medio_ponderado.values

    # Removendo a coluna 'cod_loja' se não for necessária
    vendas_agregadas = vendas_agregadas.drop(columns=['cod_loja'])
    
    return vendas_agregadas

def estimar_desconto_loja(historico, promocao_futura):
    estimativas = []
    
    # Iterar sobre cada ciclo presente nas promoções futuras
    for ciclo in promocao_futura['ano_ciclo'].unique():
        produtos_promocao = promocao_futura[promocao_futura['ano_ciclo'] == ciclo]
        
        # Ponderar o desconto de cada produto com base nas vendas históricas da loja
        desconto_medio_ponderado_ciclo = 0
        soma_pesos = 0
        
        for _, produto in produtos_promocao.iterrows():
            cod_produto = produto['cod_produto']
            desconto = produto['desconto']
            
            # Calcular a participação do produto nas vendas totais do ciclo
            historico_produto = historico[historico['cod_produto'] == cod_produto]
            if not historico_produto.empty:
                # Aqui, usamos o histórico para estimar a participação do produto nas vendas da loja
                peso = historico_produto['num_vendas'].sum() / historico['num_vendas'].sum()
            else:
                peso = 0
            
            desconto_medio_ponderado_ciclo += desconto * peso
            soma_pesos += peso

        # Se houver pesos, ajusta o desconto ponderado
        if soma_pesos > 0:
            desconto_medio_ponderado_ciclo /= soma_pesos

        estimativas.append({
            'ano_ciclo': ciclo,
            'descontoMedio_ponderado': desconto_medio_ponderado_ciclo
        })

    # Converter para DataFrame e garantir que os ciclos não se repitam
    estimativas_df = DataFrame(estimativas)
    
    return estimativas_df