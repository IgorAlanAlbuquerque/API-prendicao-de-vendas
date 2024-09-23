import unittest
from flask import Flask, session
from flask.testing import FlaskClient
from routes.session_route import session_bp 

class TestSessionCookie(unittest.TestCase):

    def setUp(self):
        # Cria uma instância do Flask e registra o blueprint
        self.app = Flask(__name__)
        self.app.secret_key = 'supersecretkey'  # Necessário para a sessão funcionar
        self.app.register_blueprint(session_bp)
        self.app.config['TESTING'] = True  # Configura o app para modo de teste

        # Cria um cliente de teste
        self.client = self.app.test_client()

        # Contexto de aplicação necessário para manipular 'session'
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Remove o contexto da aplicação após o teste
        self.app_context.pop()

    def test_get_session_cookie(self):
        # Faz a requisição GET para a rota que cria o cookie de sessão
        response = self.client.get('/get-session-cookie')

        # Verifica se o status da resposta é 200 (sucesso)
        self.assertEqual(response.status_code, 200)

        # Verifica se a mensagem no JSON é correta
        self.assertEqual(response.json['message'], "Cookie de sessão criado")

        # Verifica se a sessão foi configurada corretamente
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['user'], 'backend')

if __name__ == '__main__':
    unittest.main()
