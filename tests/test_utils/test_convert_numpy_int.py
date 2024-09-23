import unittest
import numpy as np
from utils.convert_numpy_int import converter_previsoes, converter_numpy  # Substitua pelo caminho correto

class TestConverterPrevisoes(unittest.TestCase):

    def test_converter_numpy(self):
        # Testando conversão de np.integer
        val = np.int32(10)
        result = converter_numpy(val)
        self.assertEqual(result, 10)
        self.assertIsInstance(result, int)

        # Testando conversão de np.floating
        val = np.float64(10.5)
        result = converter_numpy(val)
        self.assertEqual(result, 10.5)
        self.assertIsInstance(result, float)

        # Testando conversão de np.ndarray
        val = np.array([1, 2, 3])
        result = converter_numpy(val)
        self.assertEqual(result, [1, 2, 3])
        self.assertIsInstance(result, list)

        # Testando outro tipo que não seja numpy
        val = "string"
        result = converter_numpy(val)
        self.assertEqual(result, "string")
        self.assertIsInstance(result, str)

    def test_converter_previsoes(self):
        # Estrutura de exemplo
        previsoes = {
            'lojas': [
                {
                    'cod_loja': 123,
                    'produtos': [
                        {
                            'cod_produto': 456,
                            'previsoes': [
                                {'previsao': np.int32(100)},
                                {'previsao': np.float64(200.5)}
                            ]
                        }
                    ]
                }
            ]
        }

        # Executar a conversão
        result = converter_previsoes(previsoes)

        # Verificar se os códigos de loja e produto foram convertidos para string
        self.assertEqual(result['lojas'][0]['cod_loja'], '123')
        self.assertEqual(result['lojas'][0]['produtos'][0]['cod_produto'], '456')

        # Verificar se as previsões foram convertidas corretamente
        self.assertEqual(result['lojas'][0]['produtos'][0]['previsoes'][0]['previsao'], 100)
        self.assertIsInstance(result['lojas'][0]['produtos'][0]['previsoes'][0]['previsao'], int)

        self.assertEqual(result['lojas'][0]['produtos'][0]['previsoes'][1]['previsao'], 200.5)
        self.assertIsInstance(result['lojas'][0]['produtos'][0]['previsoes'][1]['previsao'], float)

if __name__ == '__main__':
    unittest.main()
