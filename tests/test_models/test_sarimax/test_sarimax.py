import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from models.sarimax.sarimax import sarimax

class TestSarimax(unittest.TestCase):

    @patch('models.sarimax.sarimax.treinar_modelo')  # Mock para a função treinar_modelo
    @patch('models.sarimax.sarimax.desagregar_previsao')  # Mock para a função desagregar_previsao
    @patch('models.sarimax.sarimax.agregar')  # Mock para a função agregar
    @patch('models.sarimax.sarimax.estimar_desconto_loja')  # Mock para a função estimar_desconto_loja
    @patch('models.sarimax.sarimax.indexar_loja')  # Mock para a função indexar_loja
    @patch('models.sarimax.sarimax.separar_ciclos')  # Mock para a função separar_ciclos
    def test_sarimax(self, mock_separar_ciclos, mock_indexar_loja, mock_estimar_desconto_loja, mock_agregar, mock_desagregar_previsao, mock_treinar_modelo):
        # Dados de exemplo
        df = pd.DataFrame({
            'cod_loja': ['loja1', 'loja1'],
            'cod_produto': ['prod1', 'prod2'],
            'ano_ciclo': [202301, 202301],
            'num_vendas': [100, 200],
            'descontoMedio': [0.1, 0.15]
        })
        
        promocao_futura = pd.DataFrame({
            'cod_loja': ['loja1', 'loja1'],
            'cod_produto': ['prod1', 'prod2'],
            'ano_ciclo': [202302, 202302],
            'desconto': [0.05, 0.1]
        })
        
        # Mocks
        mock_separar_ciclos.return_value = (2023, 1, 2022, 12)
        mock_indexar_loja.side_effect = lambda x: x
        mock_agregar.return_value = pd.DataFrame({
            'ano_ciclo': [202301],
            'num_vendas': [300],
            'descontoMedio_ponderado': [0.12]
        })
        mock_estimar_desconto_loja.return_value = pd.DataFrame({
            'ano_ciclo': [202302],
            'descontoMedio_ponderado': [0.08]
        })
        mock_treinar_modelo.return_value = pd.Series([310])
        mock_desagregar_previsao.return_value = [150, 160]

        # Executar a função
        result = sarimax(df, promocao_futura)

        # Verificações
        self.assertIn('lojas', result)
        self.assertEqual(len(result['lojas']), 1)
        
        loja1 = result['lojas'][0]
        self.assertEqual(loja1['cod_loja'], 'loja1')
        self.assertEqual(len(loja1['produtos']), 2)

        # Verificar previsões de produtos
        produto1 = loja1['produtos'][0]
        self.assertEqual(produto1['cod_produto'], 'prod1')
        self.assertEqual(len(produto1['previsoes']), 1)
        self.assertEqual(produto1['previsoes'][0]['previsao'], 150)
        
        # Verificar se as funções foram chamadas
        mock_separar_ciclos.assert_called_once()
        mock_agregar.assert_called()
        mock_estimar_desconto_loja.assert_called()
        mock_treinar_modelo.assert_called()
        mock_desagregar_previsao.assert_called()

if __name__ == '__main__':
    unittest.main()
