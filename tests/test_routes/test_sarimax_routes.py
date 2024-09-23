import unittest
from unittest.mock import patch
from flask import Flask
from routes.sarimax_route import sarimax_bp  # Substitua pelo caminho correto do blueprint

class TestPreverVendasSarimax(unittest.TestCase):

    def setUp(self):
        # Cria uma instância do Flask e registra o blueprint
        self.app = Flask(__name__)
        self.app.register_blueprint(sarimax_bp)
        self.app.config['TESTING'] = True

        # Cria um cliente de teste
        self.client = self.app.test_client()

    @patch('routes.sarimax_route.carregar_arquivos')  # Mock da função carregar_arquivos
    @patch('routes.sarimax_route.service_sarimax')  # Mock da função service_sarimax
    @patch('routes.sarimax_route.converter_previsoes')  # Mock da função converter_previsoes
    def test_prever_vendas_sarimax(self, mock_converter_previsoes, mock_service_sarimax, mock_carregar_arquivos):
        # Mockar o retorno de carregar_arquivos para simular o carregamento de arquivos correto
        mock_carregar_arquivos.return_value = (["data1"], ["data2"], None, 200)
        
        # Mockar o retorno de service_sarimax para simular uma previsão
        mock_service_sarimax.return_value = [10, 20, 30]

        # Mockar o retorno de converter_previsoes para simular a conversão das previsões
        mock_converter_previsoes.return_value = [10, 20, 30]

        # Fazer uma requisição POST para a rota
        response = self.client.post("/prever-vendas/")

        # Verificar o status da resposta
        self.assertEqual(response.status_code, 200)

        # Verificar o conteúdo da resposta
        self.assertEqual(response.json, [10, 20, 30])

        # Verificar se as funções foram chamadas corretamente
        mock_carregar_arquivos.assert_called_once()
        mock_service_sarimax.assert_called_once_with(["data1"], ["data2"])
        mock_converter_previsoes.assert_called_once_with([10, 20, 30])

    @patch('routes.sarimax_route.carregar_arquivos')  # Mock da função carregar_arquivos
    def test_prever_vendas_sarimax_error(self, mock_carregar_arquivos):
        # Mockar o retorno de carregar_arquivos para simular um erro no carregamento de arquivos
        mock_carregar_arquivos.return_value = (None, None, {"error": "Invalid file"}, 400)

        # Fazer uma requisição POST para a rota
        response = self.client.post("/prever-vendas/")

        # Verificar o status da resposta
        self.assertEqual(response.status_code, 400)

        # Verificar o conteúdo da resposta de erro
        self.assertEqual(response.json, {"error": "Invalid file"})

        # Verificar se a função carregar_arquivos foi chamada corretamente
        mock_carregar_arquivos.assert_called_once()

if __name__ == '__main__':
    unittest.main()
