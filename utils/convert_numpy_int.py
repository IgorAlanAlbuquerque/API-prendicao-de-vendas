from math import ceil

def converter_previsoes(data):
    for loja in data:
        loja['cod_loja'] = int(loja['cod_loja'])
        for produto in loja['produtos']:
            produto['cod_produto'] = int(produto['cod_produto'])
            for previsao in produto['previsoes']:
                previsao['ciclo'] = int(previsao['ciclo'])
                previsao['previsao'] = int(ceil(float(previsao['previsao'])))
    return data

'''
exemplo da estrutura do retorno
[
    {
        'cod_loja':123,
        'produtos':[
            {
                'cod_produto':567,
                'previsoes':[
                    {
                        'ano_ciclo':202410,
                        'previsao':11  
                    },
                    {
                        'ano_ciclo':202411,
                        'previsao':8
                    }
                ]
            },
            {
                'cod_produto':688.
                'previsoes':[...]
            }
        ]
        
    },
    {
        'cod_loja':321,
        'produtos:[...] 
    }
    
]
'''