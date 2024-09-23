from models.sarimax.sarimax import sarimax

def service_sarimax(data1, data2):
    p = sarimax(data1, data2)
    return p