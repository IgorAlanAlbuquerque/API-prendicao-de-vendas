from models.exponencial.exponencial import exponencial
PERIODO = 3
PESO_A = 1
PESO_B = 1
def service_exponencial(data1, data2):
    p = exponencial(data1, data2, PERIODO, PESO_A, PESO_B)
    return p