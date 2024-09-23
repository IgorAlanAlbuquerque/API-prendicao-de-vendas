def media_ponderada_ema2(df_ema, df_ciclos, a, b):
    return (a * df_ema + b * df_ciclos) / (a + b)