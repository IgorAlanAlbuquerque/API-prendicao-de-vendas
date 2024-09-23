from pandas import concat, DataFrame
from .utils import calcular_erro
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from math import ceil
from numpy import random

def desagregar(historico, ciclo, pesos):
    ciclos_equivalentes = [ciclo - j*100 for j in range(1, 4)]
    if ciclo%100 >= 4:
        ciclos_anteriores = [ciclo - j for j in range(1, 4)]
    else:
        ciclos_anteriores = [ciclo - j for j in range(1, ciclo%100)]
        ano_anterior = (ciclo//100)-1
        ano_ciclo_anterior = ano_anterior*100+17
        ant = [ano_ciclo_anterior - j for j in range(0, (ciclo%100)*(-1)+4)]
        ciclos_anteriores.extend(ant)
    
    ciclos_relevantes = DataFrame({
        'ciclos': ciclos_equivalentes + ciclos_anteriores,
        'pesos': pesos  # Aqui usamos os pesos otimizados
    })
    
    historico_relevante = historico[historico['ano_ciclo'].isin(ciclos_relevantes['ciclos'].tolist())].copy()
    historico_relevante = historico_relevante.merge(ciclos_relevantes, left_on='ano_ciclo', right_on='ciclos',
                                                    how='left')
    
    if not historico_relevante.empty:
        historico_relevante['ponderacao'] = historico_relevante['num_vendas_produto'] * historico_relevante['pesos']
        media_contribuicao = historico_relevante['ponderacao'].sum() / (historico_relevante
                                                                       ['num_vendas']*historico_relevante
                                                                       ['pesos']).sum()
    else:
        media_contribuicao = 0
            
    return media_contribuicao


def desagregar_previsao(loja, vendas_agregadas, produtos, ciclo, pesos):
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
        produto_taxa = desagregar(historico_produto, ciclo, pesos)
        produto_taxa = float(produto_taxa)

        # Calcula a parte do produto na previsão total
        divisoes.append(produto_taxa)
        
    # Normalizar as divisões para que a soma seja igual a 1
    soma_divisoes = sum(divisoes)
    if soma_divisoes > 1:
        divisoes = [divisao / soma_divisoes for divisao in divisoes]
        
    return divisoes


def desagregar_bayse(loja_pra_prever, vendas_agregadas, produtos, ciclo_pra_prever, previsto):
    # Função que será otimizada
    if ciclo_pra_prever%100 >= 4:
        ciclos_anteriores = [ciclo_pra_prever - j for j in range(1, 4)]
    else:
        ciclos_anteriores = [ciclo_pra_prever - j for j in range(1, ciclo_pra_prever%100)]
        ano_anterior = (ciclo_pra_prever//100)-1
        ano_ciclo_anterior = ano_anterior*100+17
        ant = [ano_ciclo_anterior - j for j in range(0, (ciclo_pra_prever%100)*(-1)+4)]
        ciclos_anteriores.extend(ant)

    #ciclo anterior 1
    total_loja_anterior1 = vendas_agregadas[vendas_agregadas['ano_ciclo'] == ciclos_anteriores[0]]['num_vendas']
    loja_ciclo_anterior1 = loja_pra_prever[loja_pra_prever['ano_ciclo'] == ciclos_anteriores[0]]
    taxa_real1 = [loja_ciclo_anterior1[loja_ciclo_anterior1['cod_produto'] == produto]['num_vendas'].
                  values[0] / total_loja_anterior1 for produto in produtos]
    #ciclo anterior 2
    total_loja_anterior2 = vendas_agregadas[vendas_agregadas['ano_ciclo'] == ciclos_anteriores[1]]['num_vendas']
    loja_ciclo_anterior2 = loja_pra_prever[loja_pra_prever['ano_ciclo'] == ciclos_anteriores[1]]
    taxa_real2 = [loja_ciclo_anterior2[loja_ciclo_anterior2['cod_produto'] == produto]['num_vendas'].
                  values[0] / total_loja_anterior2 for produto in produtos]
    #ciclo anterior 3
    total_loja_anterior3 = vendas_agregadas[vendas_agregadas['ano_ciclo'] == ciclos_anteriores[2]]['num_vendas']
    loja_ciclo_anterior3 = loja_pra_prever[loja_pra_prever['ano_ciclo'] == ciclos_anteriores[2]]
    taxa_real3 = [loja_ciclo_anterior3[loja_ciclo_anterior3['cod_produto'] == produto]['num_vendas'].
                  values[0] / total_loja_anterior3 for produto in produtos]
    taxa_real =taxa_real1+taxa_real2+taxa_real3
        
    def objective(space):
        pesos = space['pesos']
        previsao1 = desagregar_previsao(loja_pra_prever, vendas_agregadas, produtos, ciclos_anteriores[0], pesos)
        previsao2 = desagregar_previsao(loja_pra_prever, vendas_agregadas, produtos, ciclos_anteriores[1], pesos)
        previsao3 = desagregar_previsao(loja_pra_prever, vendas_agregadas, produtos, ciclos_anteriores[2], pesos)

        previsao = previsao1+previsao2+previsao3
    
        # Calcular o erro entre previsão e a taxa real
        erro = calcular_erro(previsao, taxa_real)
        
        return {'loss': erro, 'status': STATUS_OK}

    space = {
    'pesos': [hp.uniform(f'peso_{i}', 0.1, 5) for i in range(6)]  # 6 pesos individuais
    }

    # Definindo o gerador de números aleatórios com um estado fixo
    random_state = random.default_rng(42)
    trials = Trials()
    # Realizando a busca com random_state
    best = fmin(fn=objective,
                space=space,
                algo=tpe.suggest,
                max_evals=100,  # Número de iterações
                trials=trials,
                rstate=random_state,
                show_progressbar=False)

    pesos_ajustados = [best[f'peso_{i}'] for i in range(6)]
    divisoes = desagregar_previsao(loja_pra_prever, vendas_agregadas, produtos, ciclo_pra_prever, pesos_ajustados)
    divisoes = [ceil(taxa * previsto) for taxa in divisoes]

    return divisoes