from flask import Blueprint, jsonify
from service.service_sarimax import service_sarimax
from utils.file_loader import carregar_arquivos
from utils.convert_numpy_int import converter_previsoes

# Definir o blueprint para as rotas SARIMAX
sarimax_bp = Blueprint('sarimax_bp', __name__)

# Rota para previsão de vendas usando o método SARIMAX
@sarimax_bp.route("/prever-vendas/", methods=["POST"])
def prever_vendas_sarimax():
    # Carregar e verificar os arquivos enviados na requisição
    data1, data2, error_response, status_code = carregar_arquivos()
    if error_response:
        return error_response, status_code

    # Processar os dados com o método SARIMAX
    previsoes = service_sarimax(data1, data2)
    #converter os tipos para valores serializaveis
    previsoes = converter_previsoes(previsoes)
    
    
    return jsonify(previsoes)