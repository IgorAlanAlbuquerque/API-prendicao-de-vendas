from models.exponencial.exponencial import exponencial

def service_exponencial(data1, data2):
    p = exponencial(data1, data2, 3, 1, 1)
    return p