from pandas import concat
from .bayse import sarima_bayse
from .sarimax_model import sarimax_model

def treinar_modelo(train, test, estimado, num_pred):
    melhor = sarima_bayse(train['num_vendas'], train['descontoMedio_ponderado'], test['descontoMedio_ponderado'],
                          test['num_vendas'], len(test['num_vendas']))
    if melhor is None:
        return None
    
    model = sarimax_model(concat([train['num_vendas'], test['num_vendas']]),
                      (melhor[0], melhor[1], melhor[2]),
                      (melhor[3], melhor[4], melhor[5], 17),
                      concat([train['descontoMedio_ponderado'], test['descontoMedio_ponderado']]))
    #fazer predicao
    forecast = model.get_forecast(steps=num_pred, exog=estimado['descontoMedio_ponderado'])
    result = forecast.predicted_mean
    return result