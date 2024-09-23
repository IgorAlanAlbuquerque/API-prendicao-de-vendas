from .med_exp_loop import prever_ciclos_futuros


def exponencial(df, promocao_futura, periodo, peso_a, peso_b):
    # Ordenar os dados por ano_ciclo
    df = df.sort_values(by='ano_ciclo')
    #json de previsao por loja
    previsao_json = {
        'lojas': []
    }
    ciclos_prever = len(promocao_futura['ano_ciclo'].unique())
    for loja in df['cod_loja'].unique():
        #json da loja
        json_loja = {
            'cod_loja':loja,
            'produtos':[]
        }
        
        #adicionar os produtos de cada loja
        produtos = promocao_futura[promocao_futura['cod_loja'] == loja]['cod_produto'].unique()
        for produto in produtos:
            json_produto = {
                'cod_produto': produto,
                'previsoes': []
            }
            json_loja['produtos'].append(json_produto)
        #filtrar dataframe por loja
        df_l = df[df['cod_loja']==loja]
        df_p = df_l[df_l['cod_produto'].isin(produtos)].copy()
        previsoes_futuras = prever_ciclos_futuros(df_p, periodo, ciclos_prever, peso_a, peso_b)
        for _, pre in previsoes_futuras.iterrows():
        # Encontra o produto correspondente no JSON da loja
            for produto in json_loja['produtos']:
                if produto['cod_produto'] == pre['cod_produto']:
                    produto['previsoes'].append(pre['previsao'])
                    
        previsao_json['lojas'].append(json_loja)
           
    return previsao_json