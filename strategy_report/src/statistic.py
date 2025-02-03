import pandas as pd

def calculate_statistics():
    # Carregar os dados
    df = pd.read_csv(file_path)
    
    # Converter a coluna 'datetime' para datetime e definir como índice
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    
    # Calcular estatísticas
    tr_portfolios = df['result']
    mean_result = tr_portfolios.mean()
    median_result = tr_portfolios.median()
    std_result = tr_portfolios.std()
    max_result = tr_portfolios.max()
    max_52_weeks = tr_portfolios.rolling(window=52*7).max().max()  # Máxima das últimas 52 semanas
    
    return {
        'mean': mean_result,
        'median': median_result,
        'std': std_result,
        'max': max_result,
        'max_52_weeks': max_52_weeks
    }

# Exemplo de uso
if __name__ == "__main__":
    file_path = 'path_to_your_data.csv'  # Substitua pelo caminho do seu arquivo de dados
    stats = calculate_statistics(file_path)
    print(stats)