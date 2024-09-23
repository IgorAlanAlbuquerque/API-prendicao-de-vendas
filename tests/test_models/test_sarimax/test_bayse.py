import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from models.sarimax.bayse import sarima_bayse

class TestSarimaBayse(unittest.TestCase):

    @patch('models.sarimax.bayse.metrica')  # Mock para a função metrica
    @patch('models.sarimax.bayse.sarimax_model')  # Mock para a função sarimax_model
    def test_sarima_bayse(self, mock_sarimax_model, mock_metrica):
        # Dados de exemplo
        treino = pd.Series([100, 110, 120, 130, 140])
        exo = pd.Series([0, 0.1, 0.2, 0.3, 0.4])
        t_exo = pd.Series([0.5, 0.6])
        teste = pd.Series([150, 160])
        n_p = 2

        # Configurando o retorno do mock de sarimax_model
        mock_model_instance = MagicMock()
        mock_forecast = MagicMock()
        mock_forecast.predicted_mean = pd.Series([155, 165])  # Mock de valores de previsão
        mock_model_instance.get_forecast.return_value = mock_forecast
        mock_sarimax_model.return_value = mock_model_instance

        # Configurando o retorno do mock de metrica
        mock_metrica.return_value = 0.5  # Mock de valor de métrica

        # Executar a função
        result = sarima_bayse(treino, exo, t_exo, teste, n_p)

        # Verificar se sarimax_model foi chamado corretamente
        mock_sarimax_model.assert_called()

        # Verificar se metrica foi chamada corretamente
        mock_metrica.assert_called()

        # Verificar o resultado final
        self.assertEqual(result, [6, 0, 2, 2, 1, 0])

    @patch('models.sarimax.bayse.gp_minimize')
    def test_sarima_bayse_failure(self, mock_gp_minimize):
        # Configurar o mock para levantar uma exceção
        mock_gp_minimize.side_effect = Exception("Erro no gp_minimize")

        # Dados de exemplo
        treino = pd.Series([100, 110, 120, 130, 140])
        exo = pd.Series([0, 0.1, 0.2, 0.3, 0.4])
        t_exo = pd.Series([0.5, 0.6])
        teste = pd.Series([150, 160])
        n_p = 2

        # Executar a função
        result = sarima_bayse(treino, exo, t_exo, teste, n_p)

        # Verificar se o resultado é None devido à exceção
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()