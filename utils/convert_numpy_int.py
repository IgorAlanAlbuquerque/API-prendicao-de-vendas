from numpy import integer, ndarray, floating

def converter_numpy(val):
    if isinstance(val, integer):
        return int(val)
    elif isinstance(val, floating):
        return float(val)
    elif isinstance(val, ndarray):
        return val.tolist()
    else:
        return val

# Função para garantir que cod_loja e cod_produto sejam strings
def converter_previsoes(previsoes):
    for loja in previsoes['lojas']:
        loja['cod_loja'] = str(loja['cod_loja'])
        for produto in loja['produtos']:
            produto['cod_produto'] = str(produto['cod_produto'])
            for previsao in produto['previsoes']:
                previsao['previsao'] = converter_numpy(previsao['previsao'])
    return previsoes