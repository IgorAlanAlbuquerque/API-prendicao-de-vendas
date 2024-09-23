import unittest
from unittest.mock import patch
from service.service_sarimax import service_sarimax  # Substitua pelo caminho correto da função

class TestServiceExponencial(unittest.TestCase):

    @patch('service.service_sarimax.sarimax')  # Mockando a função exponencial
    def test_service_exponencial(self, mock_exponencial):
        # Configurando o retorno do mock da função exponencial
        mock_exponencial.return_value = 42  # Valor fictício de retorno

        # Dados de exemplo para o teste
        data1 = [1, 2, 3]
        data2 = [4, 5, 6]

        # Chamando a função que estamos testando
        result = service_sarimax(data1, data2)

        # Verificando se a função exponencial foi chamada com os parâmetros corretos
        mock_exponencial.assert_called_once_with(data1, data2)

        # Verificando o retorno da função
        self.assertEqual(result, 42)

if __name__ == '__main__':
    unittest.main()