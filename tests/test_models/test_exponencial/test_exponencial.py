import unittest
import pandas as pd
from models.exponencial.exponencial import exponencial

class TestExponencial(unittest.TestCase):
    def setUp(self):
        # Dados de exemplo para a função
        self.df = pd.DataFrame({
            'cod_loja': ['L1', 'L1', 'L1', 'L1', 'L1', 'L1', 'L1', 'L1', 'L1', 'L1', 'L1', 'L1', 'L1', 'L1', 'L1', 'L1', 'L1', 'L1'],
            'cod_produto': ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
            'ano_ciclo': [202114, 202115, 202214, 202215, 202314, 202315, 202411, 202412, 202413, 202114, 202115, 202214, 202215, 202314, 202315, 202411, 202412, 202413],
            'num_vendas': [100, 150, 200, 100, 120, 80, 80, 130, 180, 100, 150, 120, 90, 130, 120, 110, 110, 70]
        })

        self.promocao_futura = pd.DataFrame({
            'cod_loja': ['L1', 'L1', 'L1', 'L1'],
            'cod_produto': ['A', 'A', 'B', 'B'],
            'ano_ciclo': [202414, 202415, 202414, 202415],
            'promocao': [0.1, 0.2, 0.0, 0.2]
        })

        self.periodo = 3
        self.peso_a = 2
        self.peso_b = 1

    def test_exponencial(self):
        # Chamada da função exponencial
        resultado = exponencial(self.df, self.promocao_futura, self.periodo, self.peso_a, self.peso_b)

        # Estrutura esperada do resultado
        resultado_esperado = {
            'lojas': [
                {
                    'cod_loja': 'L1',
                    'produtos': [
                        {
                            'cod_produto': 'A',
                            'previsoes': [128.75, 102.70833333333333]
                        },
                        {
                            'cod_produto': 'B',
                            'previsoes': [118.75, 119.375]
                        }
                    ]
                }
            ]
        }

        # Verificar se o resultado retornado é o esperado
        self.assertEqual(resultado, resultado_esperado)

if __name__ == '__main__':
    unittest.main()
