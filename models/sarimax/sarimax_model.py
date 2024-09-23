from statsmodels.tsa.statespace.sarimax import SARIMAX
from numpy import random

def sarimax_model(y, order, seasonal_order, exog=None):
    try:
      random.seed(42)
      model = SARIMAX(y, exog=exog, order=order, seasonal_order=seasonal_order)
      result = model.fit(maxiter=100, disp=False) #100
      return result
    except Exception:
          return None