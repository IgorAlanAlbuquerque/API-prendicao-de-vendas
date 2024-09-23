import unittest
import pandas as pd
from models.sarimax.agregar import agregar, estimar_desconto_loja

class TestUtils(unittest.TestCase):

    def setUp(self):
        # Setup inicial dos dados para os testes
        self.loja_data = pd.DataFrame({
            'cod_loja': ['loja1', 'loja1', 'loja1', 'loja1'],
            'ano_ciclo': [202301, 202301, 202302, 202302],
            'cod_produto': ['produto1', 'produto2', 'produto1', 'produto2'],
            'num_vendas': [100, 200, 150, 50],
            'descontoMedio': [0.1, 0.2, 0.15, 0.25]
        })
        
        self.promocao_futura_data = pd.DataFrame({
            'ano_ciclo': [202303, 202303],
            'cod_produto': ['produto1', 'produto2'],
            'desconto': [0.2, 0.3]
        })
    
    def test_agregar(self):
        # Testar se a função 'agregar' retorna o resultado esperado
        result = agregar(self.loja_data)
        
        # Verificar se o DataFrame de vendas agregadas está correto
        expected_vendas_agregadas = pd.DataFrame({
            'ano_ciclo': [202301, 202302],
            'num_vendas': [300, 200],
            'descontoMedio_ponderado': [0.16666666666666666, 0.175]
        })
        
        # Comparar se as colunas 'ano_ciclo' e 'num_vendas' do resultado são como esperado
        pd.testing.assert_frame_equal(result, expected_vendas_agregadas)
        
    
    def test_estimar_desconto_loja(self):
        # Testar se a função 'estimar_desconto_loja' retorna os valores corretos
        result = estimar_desconto_loja(self.loja_data, self.promocao_futura_data)
        
        # Verificar se o desconto médio ponderado está correto
        expected_result = pd.DataFrame({
            'ano_ciclo': [202303],
            'descontoMedio_ponderado': [0.25]  # valor estimado esperado
        })
        
        # Comparar os resultados das estimativas
        pd.testing.assert_frame_equal(result, expected_result)
        
if __name__ == '__main__':
    unittest.main()
        