import json
import pandas as pd
from plotly import graph_objs as go

def create_monthly_returns():

    # Ler arquivo data/portfolio_14.json
    with open('./data/monthly_returns.json') as f:
        data = json.load(f)    
    df = pd.DataFrame(data)

    # Transpose dataframe
    df = df.T
    df = df.round(2)

    # Inverter a ordem dos anos
    df = df.iloc[::-1]

    print(df)


    # Gerar um heatmap com cores personalizadas e valores exibidos
    trace = go.Heatmap(
        z=df.values.tolist(),
        x=df.columns,
        y=df.index,
        colorscale=[
                [0, '#FF0000'],  # Vermelho para valores baixos (negativos)
                [0.5, '#FFFFFF'],  # Branco para valores próximos de zero
                [1, '#1EB866']  # Verde para valores altos (positivos)
            ],
        zmin=-10,  # Valor mínimo para a escala de cores
        zmax=10,  # Valor máximo para a escala de cores
        colorbar=dict(title='Retornos'),  # Legenda para o heatmap
        text=df.values.tolist(),  # Adicionar os valores como texto
        texttemplate="%{text:.2f}",  # Formatar a exibição dos valores para duas casas decimais
        showscale=True  # Mostrar a escala de cores
    )
    
    layout = go.Layout(
        title='Retornos mensais',
        xaxis=dict(title='Meses'),
        yaxis=dict(title='Anos'),
        plot_bgcolor='white',  # Fundo branco
        paper_bgcolor='white',  # Fundo branco
        width=1200,  # Largura do gráfico em pixels para A4
        height=400,  # Altura do gráfico em pixels para A4
        # margin=dict(l=20, r=20, t=20, b=20)  # Ajustar margens conforme necessário
    )
    
    fig = go.Figure(data=[trace], layout=layout)

    return fig



create_monthly_returns()