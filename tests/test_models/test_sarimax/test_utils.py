import unittest
import pandas as pd
import numpy as np
from pandas import to_datetime
from models.sarimax.utils import load_data_ciclos, define_index, indexar_loja, separar_ciclos, metrica
from unittest.mock import patch, mock_open
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

class TestUtils(unittest.TestCase):

    # Teste para load_data_ciclos
    @patch('builtins.open', new_callable=mock_open, read_data="2021-01-01 2021-02-01 2021-03-01")
    @patch('models.sarimax.utils.path')
    def test_load_data_ciclos(self, mock_path, mock_file):
        mock_path.dirname.return_value = ''
        mock_path.abspath.return_value = ''
        result = load_data_ciclos()
        expected = to_datetime(['2021-01-01', '2021-02-01', '2021-03-01'])
        pd.testing.assert_index_equal(result, expected)

    # Teste para define_index
    def test_define_index(self):
        result = define_index(202101)
        expected = pd.Timestamp('2020-12-26')
        self.assertEqual(result, expected)

    # Teste para indexar_loja
    def test_indexar_loja(self):
        df = pd.DataFrame({
            'ano_ciclo': [202101, 202102],
            'num_vendas': [100, 200],
            'descontoMedio_ponderado': [0.1, 0.2]
        })
        result = indexar_loja(df)
        self.assertEqual(result.index.freqstr, 'D')
        self.assertEqual(result.index[0], pd.Timestamp('2020-12-26'))
    
    # Teste para separar_ciclos
    def test_separar_ciclos(self):
        df = pd.DataFrame({
            'ano_ciclo': [202117, 202201, 202202, 202203, 202204]
        })
        ano_final, ciclo_final, ano_treino, ciclo_treino = separar_ciclos(df)
        self.assertEqual(ano_final, 2022)
        self.assertEqual(ciclo_final, 4)
        self.assertEqual(ano_treino, 2022)
        self.assertEqual(ciclo_treino, 1)  # ciclo_treino foi calculado corretamente

    # Teste para metrica
    def test_metrica(self):
        teste = np.array([100, 200, 300])
        result = np.array([110, 190, 290])
        metric_result = metrica(teste, result)
        expected = 0.2 * mean_absolute_percentage_error(teste, result) + \
                   0.5 * mean_squared_error(teste, result) + \
                   0.3 * mean_absolute_error(teste, result)
        self.assertAlmostEqual(metric_result, expected)

if __name__ == '__main__':
    unittest.main()
