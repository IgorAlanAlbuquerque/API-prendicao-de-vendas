from pandas import concat
from .bayse import sarima_bayse
from .sarimax_model import sarimax_model

def treinar_modelo(train, test, estimado, num_pred):
    melhor = sarima_bayse(train['num_vendas'], train['descontoMedio_ponderado'], test['descontoMedio_ponderado'],
                          test['num_vendas'], len(test['num_vendas']))
    if melhor is None:
        return None
    model = sarimax_model(train['num_vendas'], (melhor[0], melhor[1], melhor[2]),
                          (melhor[3], melhor[4], melhor[5], 17), train['descontoMedio_ponderado'])
    #fazer predicao
    forecast = model.get_forecast(steps=num_pred+len(test['num_vendas']),
                                  exog=concat([test['descontoMedio_ponderado'], estimado['descontoMedio_ponderado']]))
    result = forecast.predicted_mean
    # Descartar as primeiras `len(test['num_vendas'])` predições
    result = result[len(test['num_vendas']):]
    return result