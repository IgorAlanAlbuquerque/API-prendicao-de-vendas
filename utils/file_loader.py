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