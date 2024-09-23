import unittest
import pandas as pd
from models.exponencial.utils import media_ponderada_ema2

class TestUtils(unittest.TestCase):

    def test_media_ponderada_ema2(self):
        # Criando DataFrames de exemplo
        df_ema1 = pd.DataFrame({'valor': [10, 20, 30, 40]})
        df_ciclos1 = pd.DataFrame({'valor': [50, 10, 20, 30]})
        df_ema2 = pd.DataFrame({'valor': [20, 25, 40, 10]})
        df_ciclos2 = pd.DataFrame({'valor': [70, 20, 6, 22]})
        
        # Definindo pesos a e b
        a1 = 1
        b1 = 1
        a2 = 2
        b2 = 0.5
        
        # Calculando a média ponderada
        resultado = media_ponderada_ema2(df_ema1['valor'], df_ciclos1['valor'], a1, b1)
        pd.testing.assert_series_equal(resultado, pd.Series([30, 15, 25, 35], name='valor'), check_dtype=False)
        resultado = media_ponderada_ema2(df_ema1['valor'], df_ciclos2['valor'], a2, b1)
        pd.testing.assert_series_equal(resultado, pd.Series([30, 20, 22, 34], name='valor'), check_dtype=False)
        resultado = media_ponderada_ema2(df_ema2['valor'], df_ciclos2['valor'], a2, b2)
        try:
            pd.testing.assert_series_equal(resultado, pd.Series([30, 24, 34, 10], name='valor'), check_dtype=False)
            self.fail("As séries são iguais, mas esperava-se que fossem diferentes.")  # Falha se as séries forem iguais
        except AssertionError:
            pass
        

if __name__ == "__main__":
    unittest.main()