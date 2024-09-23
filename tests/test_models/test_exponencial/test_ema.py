import unittest
import pandas as pd
from models.exponencial.ema import calcular_ema, calcular_ema_ciclos

class TestEma(unittest.TestCase):

    def setUp(self):
        # Criar um DataFrame exemplo para os testes
        self.df = pd.DataFrame({
            'cod_produto': ['A', 'A', 'A', 'B', 'B', 'B'],
            'ano_ciclo': [202214, 202215, 202216, 202214, 202215, 202216],
            'num_vendas': [100, 150, 200, 80, 130, 180]
        })

    def test_calcular_ema(self):
        # Definir o período para o EMA
        periodo = 3

        # Executar a função para calcular o EMA
        df_resultado = calcular_ema(self.df.copy(), periodo)

        # Verificar se a coluna EMA foi criada
        self.assertIn('EMA', df_resultado.columns)

        # Verificar se o EMA foi calculado corretamente para um produto
        produto_a_ema = df_resultado[df_resultado['cod_produto'] == 'A']['EMA']
        produto_b_ema = df_resultado[df_resultado['cod_produto'] == 'B']['EMA']

        # Comparar com o cálculo manual do EMA (simulação)
        ema_manual_a = pd.Series([100, 125, 162.5], name='EMA')
        ema_manual_b = pd.Series([80, 105, 142.5], name='EMA')

        # Comparar as séries do resultado com o cálculo manual
        pd.testing.assert_series_equal(produto_a_ema.reset_index(drop=True), ema_manual_a, atol=1e-2)
        pd.testing.assert_series_equal(produto_b_ema.reset_index(drop=True), ema_manual_b, atol=1e-2)
        
        
    def test_calcular_ema_ciclos(self):
        # Definir o período para o EMA dos ciclos equivalentes
        periodo = 3
        df = pd.DataFrame({
            'cod_produto': ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'B'],
            'ano_ciclo': [202114, 202214, 202314, 202413, 202114, 202214, 202314, 202413],
            'num_vendas': [100, 150, 200, 150, 80, 130, 180, 150]
        })

        # Executar a função para calcular o EMA nos ciclos equivalentes
        df_resultado = calcular_ema_ciclos(df.copy(), periodo)

        # Verificar se a coluna EMA_ciclos foi criada
        self.assertIn('EMA_ciclos', df_resultado.columns)

        # Verificar se a filtragem dos ciclos foi feita corretamente
        ciclos_equivalentes = [202414 - i * 100 for i in range(1, 4)]
        df_filtrado = df[df['ano_ciclo'].isin(ciclos_equivalentes)]

        # Verificar se os ciclos retornados batem com os ciclos esperados
        pd.testing.assert_frame_equal(df_resultado[['cod_produto', 'ano_ciclo', 'num_vendas']],
                                      df_filtrado[['cod_produto', 'ano_ciclo', 'num_vendas']])

        # Verificar se o EMA foi calculado corretamente nos ciclos equivalentes
        produto_a_ema_ciclos = df_resultado[df_resultado['cod_produto'] == 'A']['EMA_ciclos']
        produto_b_ema_ciclos = df_resultado[df_resultado['cod_produto'] == 'B']['EMA_ciclos']

        ema_manual_a = pd.Series([100, 125, 162.5], name='EMA')
        ema_manual_b = pd.Series([80, 105, 142.5], name='EMA')
        pd.testing.assert_series_equal(produto_a_ema_ciclos.reset_index(drop=True), ema_manual_a, atol=1e-2, check_names=False)
        pd.testing.assert_series_equal(produto_b_ema_ciclos.reset_index(drop=True), ema_manual_b.reset_index(drop=True), atol=1e-2, check_names=False)

if __name__ == '__main__':
    unittest.main()