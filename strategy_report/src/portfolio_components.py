from dash import dash_table, html
import dash_bootstrap_components as dbc
import pandas as pd


def create_portfolio_components(df = None):

    #Caso o dataframe seja nulo, criar um dataframe vazio
    if df is None:
        dataframe = pd.DataFrame({
            "Estratégia": ["#1 - Hagnar", "#2 - Odger", "#3 - Odin", "#4 - O Capitão", "#5 - Sigurd"],
            "Ativo": ["WINFUT", "WINFUT", "WINFUT", "WINFUT", "WINFUT"],
            "Tipo": ["Tendencia", "Tendencia", "Tendencia", "Tendencia", "Tendencia"],
            "Volume": [5, 5, 5, 5, 5]
        })

    else:
        dataframe = df

    #Converter o dataframe em uma dbc.Table. Os valores precisam está centralizados
    table = dbc.Table.from_dataframe(dataframe, striped=True, bordered=True, hover=True, responsive=True, className="text-center")
        
    return table

