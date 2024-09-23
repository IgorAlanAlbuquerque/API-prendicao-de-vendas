from pandas import to_datetime, date_range
import os
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from numpy import mean, array
from numpy import abs as npabs

def load_data_ciclos():
    # Obter o diretório atual deste arquivo Python
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construir o caminho completo para o arquivo de dados
    file_path = os.path.join(current_dir, 'datas_inicio_ciclos.txt')
    with open(file_path, 'r') as file:
        data = file.read()
    # Converter a string em uma lista e depois em datetime
    datas_inicio_ciclos_list = data.split()
    datas_inicio_ciclos = to_datetime(datas_inicio_ciclos_list)
    return datas_inicio_ciclos


def define_index(ano_ciclo):
    datas_inicio_ciclos = load_data_ciclos()
    ano = int(ano_ciclo/100)
    ciclo = int(ano_ciclo%100)
    return datas_inicio_ciclos[(ano-2021)*17+(ciclo-1)]



def indexar_loja(vendas_agregadas):
  vendas_agregadas['index'] = vendas_agregadas['ano_ciclo'].apply(define_index)
  loja_indexada = vendas_agregadas.set_index('index')[['num_vendas', 'ano_ciclo', 'descontoMedio_ponderado']]
  if not loja_indexada.index.freq:
        loja_indexada.index = date_range(start=loja_indexada.index.min(),
                                              periods=len(loja_indexada.index),
                                              freq='D')
  return loja_indexada


def separar_ciclos(df):
    ano_final = int(df['ano_ciclo'].max() / 100)
    ciclo_final = int(df['ano_ciclo'].max() % 100)
    ano_treino = ano_final
    ciclo_treino = ciclo_final-3
    if ciclo_treino <= 0:
        ano_treino -= 1
        ciclo_treino = 17 - ciclo_treino
        
    return ano_final, ciclo_final, ano_treino, ciclo_treino

def metrica(teste, result):
  alpha = 0.2
  beta = 0.5
  gamma = 0.3
  return alpha*mean_absolute_percentage_error(teste,
                                              result)+beta*mean_squared_error(teste,
                                                                        result)+gamma*mean_absolute_error(teste,
                                                                            result)

def calcular_erro(previsao, real):
    return mean(npabs(array(previsao) - array(real)))

class SuppressPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout  # Salva o stdout original
        sys.stdout = open(os.devnull, 'w')  # Redireciona para o null
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout  # Restaura o stdout original
        
def metrica_erro_absoluto(desconto_esperado, desconto_calculado):
    return mean_absolute_error(desconto_esperado, desconto_calculado)