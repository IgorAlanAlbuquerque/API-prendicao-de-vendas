from flask import jsonify, request
from pandas import read_csv


def carregar_arquivos():
    """Carrega e verifica os arquivos enviados na requisição"""
    if 'file1' not in request.files or 'file2' not in request.files:
        return None, None, jsonify({"error": "Ambos os arquivos devem ser enviados"}), 400

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename.endswith('.csv'):
        data1 = read_csv(file1)
    else:
        return None, None, jsonify({"error": "file1 deve estar no formato CSV"}), 400

    if file2.filename.endswith('.csv'):
        data2 = read_csv(file2)
    else:
        return None, None, jsonify({"error": "file2 deve estar no formato CSV"}), 400

    return data1, data2, None, None

'''DTO - historico
cod_loja, cod_produto, ano (int), ciclo (int), num_vendas (int) (num_vendas+num_rupturas), promoção (float)

DTO - pra_prever
cod_loja, cod_produto, ano (int), ciclo (int), promoção (float)

[{
'cod_loja':[A, B, C, D],
'cod_produto':[1, 2, 1, 2],
'ano': [2024, 2024, 2024, 2024],
'ciclo': [1, 1, 2, 2],
'num_vendas':[5, 5, 11, 3],
'promocao':[0.1, 0.2, 0.25, 0.35]
},
{
'cod_loja':[A, B, C, D],
'cod_produto':[1, 2, 1, 2],
'ano': [2024, 2024, 2024, 2024],
'ciclo': [1, 1, 2, 2],
'num_vendas':[5, 5, 11, 3],
'promocao':[0.1, 0.2, 0.25, 0.35]
}
]
'''