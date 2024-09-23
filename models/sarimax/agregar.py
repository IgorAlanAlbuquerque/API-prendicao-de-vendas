from pandas import DataFrame
from bayes_opt import BayesianOptimization
from sys import stdout
from .utils import metrica_erro_absoluto, SuppressPrints

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


def estimar_desconto_loja(historico, promocao_futura, pesos_ciclos):

    estimativas = []

    for ciclo in promocao_futura['ano_ciclo'].unique():
        #ciclos equivalentes de periodos anteriores
        ciclos_equivalentes = [ciclo - j*100 for j in range(1, 4)]
        
        # Últimos 3 ciclos anteriores ao ciclo atual
        if ciclo % 100 >= 4:
            ciclos_anteriores = [ciclo - j for j in range(1, 4)]
        else:
            ciclos_anteriores = [ciclo - j for j in range(1, ciclo % 100)]
            ano_anterior = (ciclo // 100) - 1
            ano_ciclo_anterior = ano_anterior * 100 + 17
            ant = [ano_ciclo_anterior - j for j in range(0, (ciclo % 100) * (-1) + 4)]
            ciclos_anteriores.extend(ant)

        ciclos_relevantes = DataFrame({
            'ciclos': ciclos_equivalentes + ciclos_anteriores,
            'pesos': pesos_ciclos
        })
            
        # Filtra os ciclos relevantes no histórico
        historico_relevante = historico[historico['ano_ciclo'].isin(ciclos_relevantes['ciclos'].tolist())].copy()
        produtos_promocao = promocao_futura[promocao_futura['ano_ciclo'] == ciclo]

        # Merge dos ciclos relevantes com o histórico
        historico_relevante = historico_relevante.merge(ciclos_relevantes, left_on='ano_ciclo',
                                                        right_on='ciclos', how='left')
        
        # Calcular o desconto ponderado
        desconto_medio_ponderado_ciclo = 0
        
        for _, produto in produtos_promocao.iterrows():
            cod_produto = produto['cod_produto']
            desconto = produto['desconto']
            
            # Filtrar o histórico relevante para o produto atual
            historico_produto = historico_relevante[historico_relevante['cod_produto'] == cod_produto]
            if not historico_produto.empty:
                vendas_produto_ponderadas = (historico_produto['num_vendas'] * historico_produto['pesos']).sum()
                vendas_totais_ponderadas = (historico_relevante['num_vendas'] * historico_relevante['pesos']).sum()

                peso = vendas_produto_ponderadas / vendas_totais_ponderadas
            else:
                peso = 0

            desconto_medio_ponderado_ciclo += desconto * peso

        estimativas.append({
            'ano_ciclo': ciclo,
            'descontoMedio_ponderado': desconto_medio_ponderado_ciclo
        })

    return DataFrame(estimativas)

def estimar_desconto_bayse(historico, promocao_futura):
    #funcao para minimizar
    # Função que será otimizada
    ciclo_pra_prever = promocao_futura['ano_ciclo'].min()
    if ciclo_pra_prever%100 >= 4:
        ciclos_anteriores = [ciclo_pra_prever - j for j in range(1, 4)]
    else:
        ciclos_anteriores = [ciclo_pra_prever - j for j in range(1, ciclo_pra_prever%100)]
        ano_anterior = (ciclo_pra_prever//100)-1
        ano_ciclo_anterior = ano_anterior*100+17
        ant = [ano_ciclo_anterior - j for j in range(0, (ciclo_pra_prever%100)*(-1)+4)]
        ciclos_anteriores.extend(ant)

    # Selecionar os dados dos ciclos anteriores para o teste (promocao_futura_teste)
    promocao_futura_teste = historico[historico['ano_ciclo'].isin(ciclos_anteriores)].copy()
    # Selecionar o restante do histórico como treino (excluindo os ciclos anteriores)
    historico_treino = historico[~historico['ano_ciclo'].isin(ciclos_anteriores)]
    vendas_agregadas = agregar(promocao_futura_teste)
    promocao_futura_teste = promocao_futura_teste.rename(columns={'descontoMedio': 'desconto'})
    promocao_futura_teste = promocao_futura_teste.drop(columns={'num_vendas'})
    desconto_esperado = vendas_agregadas[['descontoMedio_ponderado']].values
    
    def funcao_objetivo(peso1, peso2, peso3, peso4, peso5, peso6):
        pesos = [peso1, peso2, peso3, peso4, peso5, peso6]
        
        # Calcula o desconto com os pesos atuais
        estimativas_df = estimar_desconto_loja(historico_treino, promocao_futura_teste, pesos)
        
        # Aqui você deve definir a métrica de erro, por exemplo o erro médio absoluto (MAE)
        desconto_calculado = estimativas_df['descontoMedio_ponderado'].values
        
        erro = metrica_erro_absoluto(desconto_esperado, desconto_calculado)
        
        return -erro  # Retorna o negativo para minimizar o erro

    # Otimização Bayesiana
    pbounds = {
        'peso1': (0.1, 5),  # Limites para os pesos
        'peso2': (0.1, 5),
        'peso3': (0.1, 5),
        'peso4': (0.1, 5),
        'peso5': (0.1, 5),
        'peso6': (0.1, 5)
    }
    
    optimizer = BayesianOptimization(f=funcao_objetivo, pbounds=pbounds, random_state=42)
    
    # Uso da classe SuppressPrints para suprimir prints durante a execução
    with SuppressPrints():
        optimizer.maximize(init_points=15, n_iter=100)
    
    # Exibir os melhores pesos encontrados
    melhores_pesos = optimizer.max['params']
    melhores_pesos_lista = [melhores_pesos[f'peso{i}'] for i in range(1, 7)]
    estimativas_df = estimar_desconto_loja(historico, promocao_futura, melhores_pesos_lista)
    return estimativas_df