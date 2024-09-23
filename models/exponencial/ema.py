#media exponencial de todo os historico com peso nos ultimos 3 ciclos
def calcular_ema(df, periodo):
    df['EMA'] = df.groupby('cod_produto')['num_vendas'].transform(lambda x: x.ewm(span=periodo, adjust=False).mean())
    return df

#media exponencial dos ciclos equivalentes nos periodos anteriores
def calcular_ema_ciclos(df, periodo):
    ciclo_a_prever = df['ano_ciclo'].max() + 1
    
    # Ajusta para ciclos maiores que 17 (assumindo que o ciclo máximo é 17)
    if ciclo_a_prever % 100 > 17:
        ciclo_a_prever = (ciclo_a_prever // 100) * 100 + 1
    
    # Identifica os ciclos equivalentes nos 3 anos anteriores
    ciclos_equivalentes = [ciclo_a_prever - i * 100 for i in range(1, 4)]
    
    # Filtra os dados para incluir apenas os ciclos equivalentes
    df_filtered = df[df['ano_ciclo'].isin(ciclos_equivalentes)].copy()  # Cria uma cópia explícita
    
    # Calcula a EMA para os ciclos filtrados
    df_filtered['EMA_ciclos'] = df_filtered.groupby('cod_produto')['num_vendas'].transform(
        lambda x: x.ewm(span=periodo, adjust=False).mean()
    )
    
    return df_filtered