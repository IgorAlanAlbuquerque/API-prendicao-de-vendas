import unittest
from unittest.mock import patch
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from models.sarimax.sarimax_model import sarimax_model

class TestSarimaxModel(unittest.TestCase):

    @patch('models.sarimax.sarimax_model.SARIMAX')
    def test_sarimax_model_success(self, mock_sarimax):
        # Configuração do mock SARIMAX e retorno de um valor de ajuste simulado
        mock_model = mock_sarimax.return_value
        mock_result = mock_model.fit.return_value
        mock_result.aic = 100  # Simular algum valor de retorno
        mock_model.fit.return_value = mock_result

        # Dados de exemplo para y, order e seasonal_order
        y = pd.Series([100, 110, 120, 130, 140])
        order = (1, 1, 1)
        seasonal_order = (1, 1, 1, 17)
        exog = pd.Series([1.0, 0.5, 0.3, 0.7, 0.8])

        # Executar a função
        result = sarimax_model(y, order, seasonal_order, exog)

        # Verificar se o SARIMAX foi chamado com os parâmetros corretos
        mock_sarimax.assert_called_once_with(y, exog=exog, order=order, seasonal_order=seasonal_order)

        # Verificar se a função result.fit() foi chamada
        mock_model.fit.assert_called_once_with(maxiter=100, disp=False)

        # Verificar se o resultado contém o atributo esperado
        self.assertIsNotNone(result)
        self.assertEqual(result.aic, 100)  # Verifica se o valor simulado foi retornado

    @patch('models.sarimax.sarimax_model.SARIMAX')
    def test_sarimax_model_failure(self, mock_sarimax):
        # Configuração do mock para lançar uma exceção ao tentar ajustar o modelo
        mock_sarimax.side_effect = Exception("Erro no ajuste")  # Forçar falha no ajuste do modelo

        # Dados de exemplo para y, order e seasonal_order
        y = pd.Series([100, 110, 120, 130, 140])
        order = (1, 1, 1)
        seasonal_order = (1, 1, 1, 12)
        exog = pd.Series([1.0, 0.5, 0.3, 0.7, 0.8])

        # Executar a função e verificar se ela lida corretamente com a exceção
        result = sarimax_model(y, order, seasonal_order, exog)

        # Verificar se o resultado é None, pois a exceção foi capturada
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()