import unittest
import unittest.mock
import pandas as pd
from models.exponencial.med_exp_loop import prever_ciclos_futuros

class TestPreverCiclosFuturos(unittest.TestCase):
    
    def setUp(self):
        # DataFrame de exemplo
        self.df = pd.DataFrame({
            'cod_produto': ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
            'ano_ciclo': [202114, 202115, 202214, 202215, 202314, 202315, 202411, 202412, 202413, 202114, 202115, 202214, 202215, 202314, 202315, 202411, 202412, 202413],
            'num_vendas': [100, 150, 200, 100, 120, 80, 80, 130, 180, 100, 150, 120, 90, 130, 120, 110, 110, 70]
        })
        self.periodo = 3
        self.ciclos_futuros = 2
        self.a = 2
        self.b = 1

    def test_prever_ciclos_futuros(self):
        # Chamar a função para prever os ciclos futuros
        previsoes = prever_ciclos_futuros(self.df.copy(), self.periodo, self.ciclos_futuros, self.a, self.b)

        # Verificar se as previsões estão corretas
        previsoes_esperadas = pd.DataFrame({
            'cod_produto': ['A', 'B', 'A', 'B'],
            'ano_ciclo': [202414, 202414, 202415, 202415], 
            'previsao': [127.97, 118.84, 102, 119]
        })

        pd.testing.assert_frame_equal(previsoes.reset_index(drop=True), previsoes_esperadas.reset_index(drop=True), check_dtype=False, atol=1)


if __name__ == '__main__':
    unittest.main()
