from dash import dash_table

# Define os dados da tabela
data = [
    {"Característica": "Quantidade de Estratégias", "Valor": "5"},
    {"Característica": "Ativos operados", "Valor": "2"},
    {"Característica": "Volume mínimo", "Valor": "2 contratos"},
    {"Característica": "Rebalanceamento", "Valor": "Não faz"},
    {"Característica": "Média de operações", "Valor": "2 por dia"},
    {"Característica": "Perda máxima diária", "Valor": "R$ 1.000,00"},
    {"Característica": "Plano mínimo", "Valor": "PRO"},
    {"Característica": "Capital mínimo", "Valor": "R$ 2.000,00"},
    {"Característica": "Data de início", "Valor": "13/01/2023"},
]

def create_portfolio_details():
    # Cria a tabela
    table = dash_table.DataTable(
        columns=[
            {"name": "Característica", "id": "Característica"},
            {"name": "Valor", "id": "Valor"},
        ],
        data=data,
        style_cell={'textAlign': 'center', 'padding': '5px', 'font-family': 'Poppins, sans-serif'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold', 'font-family': 'Poppins, sans-serif'},
        style_table={'width': '100%'},
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{Valor} = "PRO"',
                    'column_id': 'Valor'
                },
                'backgroundImage': 'url("/assets/pro.png")',
                'backgroundSize': '30px',  # Ajuste o tamanho da imagem aqui
                'backgroundRepeat': 'no-repeat',
                'backgroundPosition': 'center',
                'color': 'transparent'
            },
            {
                'if': {
                    'filter_query': '{Valor} = "BASIC"',
                    'column_id': 'Valor'
                },
                'backgroundImage': 'url("/assets/basic.png")',
                'backgroundSize': '30px',  # Ajuste o tamanho da imagem aqui
                'backgroundRepeat': 'no-repeat',
                'backgroundPosition': 'center',
                'color': 'transparent'
            },
            {
                'if': {
                    'filter_query': '{Valor} = "MAX"',
                    'column_id': 'Valor'
                },
                'backgroundImage': 'url("/assets/max.png")',
                'backgroundSize': '30px',  # Ajuste o tamanho da imagem aqui
                'backgroundRepeat': 'no-repeat',
                'backgroundPosition': 'center',
                'color': 'transparent'
            },
            {
                'if': {
                    'filter_query': '{Valor} = "MAX PLUS"',
                    'column_id': 'Valor'
                },
                'backgroundImage': 'url("/assets/max_p.png")',
                'backgroundSize': '30px',  # Ajuste o tamanho da imagem aqui
                'backgroundRepeat': 'no-repeat',
                'backgroundPosition': 'center',
                'color': 'transparent'
            }

        ]
    )

    return table