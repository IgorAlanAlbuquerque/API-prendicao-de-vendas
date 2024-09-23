from skopt import gp_minimize
from skopt.utils import use_named_args
from skopt.space import Integer
from .sarimax_model import sarimax_model
from .utils import metrica

def sarima_bayse(treino, exo, t_exo, teste, n_p):
  #parametros
  parametros = [
    Integer(1, 7, name='p'), #min 2
    Integer(0, 2, name='d'),
    Integer(0, 2, name='q'),
    Integer(1, 3, name='p_s'), #min 1
    Integer(0, 2, name='d_s'),
    Integer(0, 2, name='q_s'), 
    ]

  #encapsula a função objetivo passando os parametros que serão usados
  def encap_objective(treino, exo, t_exo, teste, n_p):
    @use_named_args(parametros)
    #função de minimização
    def objective(p, d, q, p_s, d_s, q_s):
      try:
          model = sarimax_model(treino, (p, d, q), (p_s, d_s, q_s, 17), exo)
          if(model==None):
              return 1e6
          forecast = model.get_forecast(steps=n_p, exog=t_exo)
          result = forecast.predicted_mean
          result_metrica = metrica(teste, result)
          return result_metrica
      except Exception:
          return 1e6
    return objective

  # método de bayse
  try:
    objective = encap_objective(treino, exo, t_exo, teste, n_p)
    result = gp_minimize(
        objective,
        parametros,
        n_calls=100,           # Número de avaliações do modelo 100
        n_random_starts=15,   # Avaliações aleatórias antes da otimização bayesiana 15
        random_state=42        # Seed para reprodutibilidade
    )
    return result.x
  except Exception:
    return None