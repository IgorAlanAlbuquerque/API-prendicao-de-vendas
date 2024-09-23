from flask import Blueprint, jsonify
from service.service_exponencial import service_exponencial
from utils.file_loader import carregar_arquivos
from utils.convert_numpy_int import converter_previsoes

# Definir o blueprint para as rotas de previsão usando o método exponencial
exponencial_bp = Blueprint('exponencial_bp', __name__)

# Rota para previsão de vendas usando o método exponencial
@exponencial_bp.route("/prever-vendas/", methods=["POST"])
def prever_vendas_exponencial():
    # Carregar e verificar os arquivos enviados na requisição
    data1, data2, error_response, status_code = carregar_arquivos()
    if error_response:
        return error_response, status_code

    # Processar os dados com o método exponencial
    previsoes = service_exponencial(data1, data2)
    previsoes = converter_previsoes(previsoes)
    
    # Retornar as previsões como JSON
    return jsonify(previsoes)