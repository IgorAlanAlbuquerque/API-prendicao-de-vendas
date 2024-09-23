import unittest
from pandas import DataFrame
from models.sarimax.desagregar import desagregar, desagregar_previsao

class TestDesagregar(unittest.TestCase):

    def setUp(self):
        # Dados de exemplo para o histórico da loja e produtos
        self.historico_produto = DataFrame({
            'cod_produto': ['produto1', 'produto1', 'produto2', 'produto2'],
            'ano_ciclo': [202301, 202302, 202301, 202302],
            'num_vendas_produto': [100, 300, 150, 50],
            'num_vendas': [250, 350, 250, 350],
            'descontoMedio': [0.1, 0.2, 0.15, 0.25]
        })

        self.vendas_agregadas = DataFrame({
            'ano_ciclo': [202301, 202302],
            'num_vendas': [250, 350],
            'descontoMedio_ponderado':[0.13, 0.207142857]
        })

        self.produtos = ['produto1', 'produto2']
        self.ciclo = 202303
        self.previsao = 500

    def test_desagregar(self):
        # Testar a função 'desagregar' com os dados de exemplo
        resultado = desagregar(self.historico_produto[self.historico_produto['cod_produto'] == 'produto1'], self.ciclo)
        
        # Verificar se o resultado está dentro de um intervalo esperado (ajustado conforme os dados)
        self.assertAlmostEqual(resultado, 0.7, delta=0.1)  # Ajuste o valor esperado conforme os dados

    def test_desagregar_previsao(self):
        # Testar a função 'desagregar_previsao' com os dados de exemplo
        local = DataFrame({
            'cod_produto': ['produto1', 'produto1', 'produto2', 'produto2'],
            'ano_ciclo': [202301, 202302, 202301, 202302],
            'num_vendas': [100, 300, 150, 50],
            'descontoMedio': [0.1, 0.2, 0.15, 0.25]
        })
        resultado = desagregar_previsao(local, self.vendas_agregadas, self.produtos, self.ciclo, self.previsao)
        
        # Verificar o tamanho da lista de divisões
        self.assertEqual(len(resultado), 2)
        
        # Verificar se as previsões somam a previsão total
        self.assertAlmostEqual(sum(resultado), self.previsao, delta=0.01)

if __name__ == '__main__':
    unittest.main()
