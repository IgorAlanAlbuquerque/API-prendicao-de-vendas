from pandas import DataFrame, concat
from .train_model import treinar_modelo
from .desagregar import desagregar_bayse
from .agregar import agregar, estimar_desconto_bayse
from .utils import separar_ciclos, indexar_loja

def sarimax(df, promocao_futura):
    num_pred = len(promocao_futura['ano_ciclo'].unique())
    
    #separar dados de treino e ajuste do modelo
    ano_final, ciclo_final, ano_treino, ciclo_treino = separar_ciclos(df)
    
    #listar lojas para fazer predição agregada
    lojas = df['cod_loja'].unique()
    
    #json de previsao por loja
    previsao_json = []
    for loja in lojas:
        #agreagar a loja
        vendas_agregadas = agregar(df[df['cod_loja']==loja])
        estimado = estimar_desconto_bayse(df[df['cod_loja']==loja],
                                          promocao_futura[promocao_futura['cod_loja']==loja])
        #indexar dados
        loja_final = indexar_loja(vendas_agregadas)
        #separar em treino e validacao
        train = loja_final[loja_final['ano_ciclo'] <= ano_treino*100+ciclo_treino]
        test = loja_final[loja_final['ano_ciclo'] > ano_treino*100+ciclo_treino]
        #treinar o modelo com os melhores parametros
        result = treinar_modelo(train, test, estimado, num_pred)
        
        #json da loja
        json_loja = {
            'cod_loja':loja,
            'produtos':[]
        }
        #se result esta vazio quer dizer que deu erro na previsao. Colocar erro no campo dessa loja
        if result is None or result.empty:
            json_loja['produtos'] = "erro"
            previsao_json.append(json_loja)
            continue
        
        resultl = result.tolist()
        #json previsao por produto
        produtos = promocao_futura[promocao_futura['cod_loja'] == loja]['cod_produto'].unique()
        
        for produto in produtos:
            json_produto = {
                'cod_produto': produto,
                'previsoes': []
            }
            json_loja['produtos'].append(json_produto)
        
        ciclos_previstos = list(range(ano_final*100+ciclo_final+1, ano_final*100+ciclo_final+num_pred+1))
        for i, ciclo in enumerate(ciclos_previstos):
            ciclo_desagregado = desagregar_bayse(df[df['cod_loja'] == loja], vendas_agregadas, produtos, ciclo,
                                                 resultl[i])
            #adicionar o ciclo previsto ao final do historico para ser usado na desagregação do proximo ciclos
            for j, pre in enumerate(ciclo_desagregado):
                # Adiciona a previsão para o produto correspondente
                json_loja['produtos'][j]['previsoes'].append({
                    'ciclo':ciclo,
                    'previsao': pre
                })
                
            # Adiciona nova linha a vendas_agregadas
            vendas_agregadas_linha = DataFrame({
                'ano_ciclo': [ciclo],
                'num_vendas': [resultl[i]],
                'descontoMedio_ponderado': [estimado.loc[estimado['ano_ciclo'] == ciclo,
                                                         'descontoMedio_ponderado'].values[0]]
            })
            vendas_agregadas = concat([vendas_agregadas, vendas_agregadas_linha], axis=0, ignore_index=True)
            
            # Adiciona novos produtos ao histórico
            desconto_medio_values = promocao_futura[promocao_futura['cod_loja'] ==
                                                    loja]['desconto'].values[:len(produtos)]
            nova_linha = DataFrame({
                'cod_loja': [loja] * len(produtos),  # Usar diretamente o valor de 'loja'
                'cod_produto': produtos,
                'ano_ciclo': [ciclo] * len(produtos),
                'num_vendas': ciclo_desagregado,
                'descontoMedio': desconto_medio_values,
            })
            # Concatena a nova linha ao DataFrame existente
            df = concat([df, nova_linha], axis=0, ignore_index=True)

        #adiciona a loja as previsões
        previsao_json.append(json_loja)
        
    return previsao_json