import unittest
from io import BytesIO
from flask import Flask
from utils.file_loader import carregar_arquivos  # Substitua pelo caminho correto do arquivo

class TestCarregarArquivos(unittest.TestCase):

    def setUp(self):
        # Cria uma instância do Flask e configura o cliente de teste
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_carregar_arquivos_sucesso(self):
        # Simula a requisição POST com dois arquivos CSV válidos
        data = {
            'file1': (BytesIO(b"col1,col2\n1,2\n3,4"), 'file1.csv'),
            'file2': (BytesIO(b"col1,col2\n5,6\n7,8"), 'file2.csv')
        }

        with self.app.test_request_context('/upload', data=data, method='POST'):
            data1, data2, error_response, status_code = carregar_arquivos()

            # Verifica se os arquivos foram carregados corretamente
            self.assertIsNotNone(data1)
            self.assertIsNotNone(data2)
            self.assertIsNone(error_response)
            self.assertIsNone(status_code)

            # Verifica o conteúdo dos arquivos
            self.assertEqual(list(data1.columns), ['col1', 'col2'])
            self.assertEqual(list(data2.columns), ['col1', 'col2'])

    def test_carregar_arquivos_faltando(self):
        # Simula a requisição POST faltando um dos arquivos
        data = {
            'file1': (BytesIO(b"col1,col2\n1,2\n3,4"), 'file1.csv')
        }

        with self.app.test_request_context('/upload', data=data, method='POST'):
            data1, data2, error_response, status_code = carregar_arquivos()

            # Verifica se a resposta de erro está correta
            self.assertIsNone(data1)
            self.assertIsNone(data2)
            self.assertIsNotNone(error_response)
            self.assertEqual(status_code, 400)

            # Verifica o conteúdo do erro
            self.assertEqual(error_response.json, {"error": "Ambos os arquivos devem ser enviados"})

    def test_carregar_arquivos_formato_invalido(self):
        # Simula a requisição POST com um arquivo no formato errado (não CSV)
        data = {
            'file1': (BytesIO(b"col1,col2\n1,2\n3,4"), 'file1.txt'),
            'file2': (BytesIO(b"col1,col2\n5,6\n7,8"), 'file2.csv')
        }

        with self.app.test_request_context('/upload', data=data, method='POST'):
            data1, data2, error_response, status_code = carregar_arquivos()

            # Verifica se a resposta de erro está correta
            self.assertIsNone(data1)
            self.assertIsNone(data2)
            self.assertIsNotNone(error_response)
            self.assertEqual(status_code, 400)

            # Verifica o conteúdo do erro para file1
            self.assertEqual(error_response.json, {"error": "file1 deve estar no formato CSV"})

if __name__ == '__main__':
    unittest.main()
