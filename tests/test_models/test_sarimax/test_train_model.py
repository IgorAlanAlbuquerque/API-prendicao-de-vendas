import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from models.sarimax.train_model import treinar_modelo 

class TestTreinarModelo(unittest.TestCase):

    @patch('models.sarimax.train_model.sarima_bayse')
    def test_treinar_modelo(self, mock_sarima_bayse):
        # Criando mocks para sarima_bayse e sarimax_model
        mock_sarima_bayse.return_value = (1, 1, 1, 1, 1, 1)  # Valor mockado para o melhor modelo
        # Dados de exemplo para train, test e estimado
        train = pd.DataFrame({
            'num_vendas': [200, 210, 220, 230],
            'descontoMedio_ponderado': [0.1, 0.15, 0.2, 0.25]
        })
        test = pd.DataFrame({
            'num_vendas': [240, 250],
            'descontoMedio_ponderado': [0.2, 0.3]
        })
        estimado = pd.DataFrame({
            'descontoMedio_ponderado': [0.25, 0.35]
        })

        # Executar a função a ser testada
        result = treinar_modelo(train, test, estimado, num_pred=2)

        # Verificar se sarima_bayse foi chamado corretamente
        mock_sarima_bayse.assert_called_once_with(train['num_vendas'], train['descontoMedio_ponderado'],
                                                  test['descontoMedio_ponderado'], test['num_vendas'],
                                                  len(test['num_vendas']))

        # Verificar o resultado final
        expected_result = pd.Series([230, 230])  # Previsões após descartar as primeiras duas (test['num_vendas'])
        pd.testing.assert_series_equal(result.reset_index(drop=True), expected_result, check_dtype=False, check_names=False)

if __name__ == '__main__':
    unittest.main()