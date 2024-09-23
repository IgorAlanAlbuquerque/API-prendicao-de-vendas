from pandas import merge, concat, DataFrame
from .ema import calcular_ema, calcular_ema_ciclos
from .utils import media_ponderada_ema2

def prever_ciclos_futuros(df, periodo, ciclos_futuros, a, b):
    # DataFrame para armazenar as previsões
    previsoes = DataFrame()
    for _ in range(ciclos_futuros):
        # Calcula a EMA com base nos dados históricos
        df_ema = calcular_ema(df.copy(), periodo)
        df_ema_ciclos = calcular_ema_ciclos(df.copy(), periodo)
    
        # Alinha os dois DataFrames pelo `cod_produto` e `ano_ciclo`
        df_ema_alinhado = df_ema[['cod_produto', 'ano_ciclo', 'EMA']]
        df_ema_ciclos_alinhado = df_ema_ciclos[['cod_produto', 'ano_ciclo', 'EMA_ciclos']]
        
        # Faz o merge dos dois DataFrames
        df_combinado = merge(df_ema_alinhado, df_ema_ciclos_alinhado, on=['cod_produto', 'ano_ciclo'], how='inner', validate='one_to_one')
        
        # Aplica a média ponderada
        df_combinado['previsao'] = media_ponderada_ema2(df_combinado['EMA'], df_combinado['EMA_ciclos'], a, b)

        # Prever o próximo ciclo para cada produto
        previsao_ciclo = df_combinado.groupby('cod_produto')['previsao'].last().reset_index()
        previsao_ciclo['ano_ciclo'] = df['ano_ciclo'].max() + 1  # Incrementa o ciclo
        
        # Adiciona a previsão ao DataFrame de previsões
        previsoes = concat([previsoes, previsao_ciclo[['cod_produto', 'ano_ciclo', 'previsao']]])
        
        # Atualiza o DataFrame original para considerar a previsão como novo valor de vendas
        df = concat([df, previsao_ciclo[['cod_produto', 'ano_ciclo', 'previsao']].rename(columns={'previsao': 'num_vendas'})])

    return previsoes