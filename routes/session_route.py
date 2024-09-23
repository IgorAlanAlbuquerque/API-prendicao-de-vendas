from flask import Blueprint, jsonify, make_response, session
from extensions import csrf

# Crie um novo blueprint para as rotas relacionadas à sessão
session_bp = Blueprint('session', __name__)

# Rota que define e retorna o cookie de sessão
@csrf.exempt  # Desabilitar CSRF apenas para essa rota
@session_bp.route('/get-session-cookie', methods=['GET'])
def get_session_cookie():
    session['user'] = 'backend'

    # Criar a resposta
    response = make_response(jsonify({"message": "Cookie de sessão criado"}))
    
    # A sessão é automaticamente armazenada no cookie pelo Flask
    return response