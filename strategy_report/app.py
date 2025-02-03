import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from src.StrategyDetails import StrategyDetails
from src.Header import Header

# Inicializa o aplicativo Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,
                                                "/assets/style.css"])


#Input do python para receber qual o strategy_id do portfólio
# strategy_id = 21
strategy_id = int(input("Digite o strategy_id: "))

# strategy_id = 155
strategy = StrategyDetails(strategy_id)

strategy_info = strategy.get_strategy_info()
fig_capital_curve, fig_monthly_returns = strategy.create_curve_capital_and_monthly_returns()
strategy_details = strategy.create_strategy_details()
fig_strategy_performance, strategy_return, cdi_return, ipca_return, bova11_return = strategy.create_strategy_performance()
stat = strategy.create_strategy_statistics()
header_class = Header(strategy_info, strategy.get_initial_end_date()[0], strategy.get_initial_end_date()[1])
header = header_class.create_header()
final_page = header_class.create_final_page()
# partner_contact = header_class.create_partner_contact()

app.layout = dbc.Container([

    html.Div(header),

    #Conteúdo
    html.Div([

        dbc.Row([
            html.Img(src='/assets/image.png')
        ]),

        html.Hr(style={'border-top': '1px solid #EAEBED'}),
        dbc.Row([
            dbc.Col([
                html.H2('Descrição comercial', className='title'),
                html.P(strategy_info[10], className='text'),
            ], className='text-container'),
            dbc.Col([
                html.H2('Descrição Técnica', className='title'),
                html.P(strategy_info[11], className='text'),
            ], className='text-container'),            
        ]),

        html.Hr(style={'border-top': '1px solid #EAEBED'}),

        dbc.Row([
            dbc.Col([
                strategy_details
            ], className='table-container'),
        ]),

        html.Hr(style={'border-top': '1px solid #EAEBED'}),


        dbc.Row([
                html.H2('Curva de capital', style={'padding': '0 50px'}, className='title'),
            dcc.Graph(     
                id='capital-curve',
                figure=fig_capital_curve,
                className='graph'
            ),
        ]),

        html.Hr(style={'border-top': '1px solid #EAEBED'}),

        dbc.Row([
                html.H2('Retornos mensais', style={'padding': '0 50px'}, className='title'),
            dcc.Graph(
                id='monthly-returns',
                figure=fig_monthly_returns,
                className='graph'
            ),
        ]),

        html.Hr(style={'border-top': '1px solid #EAEBED'}),
        #Quebra de página
        dbc.Row([
                html.H2('Benchmark', style={'padding': '0 50px'}, className='title'),
            dcc.Graph(
                id='strategy-benchmark',
                figure=fig_strategy_performance,
                className='graph'
            ),
        ]),


        dbc.Row([
            html.H2('Estatísticas', className='title'),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card17-title', className='card-title'),
                                html.P("{}".format(strategy_info[0]), id='card17-text'),
                            ]
                        ), id='card17', className='card'
                    )
                ]
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card18-title', className='card-title'),
                                html.P("CDI", id='card18-text'),
                            
                            ]
                        ), id='card18',className='card'
                    )
                ]
            ),        
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card19-title', className='card-title'),
                                html.P("IPCA", id='card19-text'),
                            ]
                        ), id='card19', className='card'
                    )
                ]
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card20-title', className='card-title'),
                                html.P("BOVA11", id='card20-text'),
                            ]
                        ), id='card20',className='card'
                    )
                ]
            ),        
        ], className='card-row'),

        dbc.Row([
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card1-title', className='card-title'),
                                html.P("Retorno Percentual", id='card1-text'),
                            ]
                        ), id='card1', className='card'
                    )
                ]
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card2-title', className='card-title'),
                                html.P("Resultado líquido", id='card2-text'),
                            
                            ]
                        ), id='card2',className='card'
                    )
                ]
            ),        
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card3-title', className='card-title'),
                                html.P("Lucro bruto", id='card3-text'),
                            ]
                        ), id='card3', className='card'
                    )
                ]
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card4-title', className='card-title'),
                                html.P("Prejuízo bruto", id='card4-text'),
                            ]
                        ), id='card4',className='card'
                    )
                ]
            ),        
        ], className='card-row'),

        dbc.Row([
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card5-title', className='card-title'),
                                html.P("Taxa de acerto", id='card5-text'),
                            ]
                        ), id='card5',className='card'
                    )
                ]
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card6-title', className='card-title'),
                                html.P("Total de operações", id='card6-text'),
                            ]
                        ), id='card6',className='card'
                    )
                ]
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card7-title', className='card-title'),
                                html.P("Operações com ganho", id='card7-text'),
                            ]
                        ), id='card7',className='card'
                    )
                ]
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card8-title', className='card-title'),
                                html.P("Operações com perda", id='card8-text'),
                            ]
                        ), id='card8',className='card'
                    )
                ]
            ),
        ], className='card-row'),

        dbc.Row([
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card9-title', className='card-title'),
                                html.P("Fator de lucro", id='card9-text'),
                            ]
                        ), id='card9',className='card'
                    )
                ]
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card10-title', className='card-title'),
                                html.P("Drawdown", id='card10-text'),
                            ]
                        ), id='card10',className='card'
                    )
                ]
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card11-title', className='card-title'),
                                html.P("Perda média", id='card11-text'),
                            ]
                        ), id='card11',className='card'
                    )
                ]
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card12-title', className='card-title'),
                                html.P("Ganho médio", id='card12-text'),
                            ]
                        ), id='card12',className='card'
                    )
                ]
            ),
        ], className='card-row'),

        dbc.Row([
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card13-title', className='card-title'),
                                html.P("Operações de compra", id='card13-text'),
                            ]
                        ), id='card13',className='card'
                    )
                ]
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card14-title', className='card-title'),
                                html.P("Operações de venda", id='card14-text'),
                            ]
                        ), id='card14',className='card'
                    )
                ]
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card15-title', className='card-title'),
                                html.P("RRR médio", id='card15-text'),
                            ]
                        ), id='card15',className='card'
                    )
                ]
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("", id='card16-title', className='card-title'),
                                html.P("Perda máxima histórica", id='card16-text'),
                            ]
                        ), id='card16',className='card'
                    )
                ]
            ),
        ], className='card-row'),

    ]),

    #Quebra de página
    html.Div(className="page-break"),
    
    html.Div(final_page)

], fluid=True, style={'padding': '0'})

@app.callback(
    [Output(f'card{i}-title', 'children') for i in range(1, 21)] + 
    [Output(f'card{i}-title', 'className') for i in range(1, 21)],
    [Input(f'card{i}-text', 'children') for i in range(1, 21)]
)
def update_cards(*args):
    card_texts = []
    formatted_stats = []
    outputs = []

    for arg in args:
        if arg == 'Retorno Percentual':
            card_texts.append("{:.2f}%".format(stat[1]))
        elif arg == 'Resultado líquido':
            card_texts.append("R$ {:.2f}".format(stat[2]))
        elif arg == 'Lucro bruto':
            card_texts.append("R$ {:.2f}".format(stat[3]))
        elif arg == 'Prejuízo bruto':
            card_texts.append("R$ {:.2f}".format(stat[4]))
        elif arg == 'Taxa de acerto':
            card_texts.append("{:.1f}%".format(stat[5]))
        elif arg == 'Total de operações':
            card_texts.append("{}".format(stat[6]))
        elif arg == 'Operações com ganho':
            card_texts.append("{}".format(stat[7]))
        elif arg == 'Operações com perda':
            card_texts.append("{}".format(stat[8]))
        elif arg == 'Fator de lucro':
            card_texts.append("{:.2f}x".format(stat[9]))
        elif arg == 'Drawdown':
            card_texts.append("{:.2f}%".format(stat[10]))
        elif arg == 'Perda média':
            card_texts.append("R$ {:.2f}".format(stat[11]))
        elif arg == 'Ganho médio':
            card_texts.append("R$ {:.2f}".format(stat[12]))
        elif arg == 'Operações de compra':
            card_texts.append("{}".format(stat[13]))
        elif arg == 'Operações de venda':
            card_texts.append("{}".format(stat[14]))
        elif arg == 'RRR médio':
            card_texts.append("{:.2f}".format(stat[15]))
        elif arg == 'Perda máxima histórica':
            card_texts.append("R$ {:.2f}".format(stat[16]))
        elif arg == '{}'.format(strategy_info[0]):
            card_texts.append("{:.2f}%".format(strategy_return))
        elif arg == 'CDI':
            card_texts.append("{:.2f}%".format(cdi_return))
        elif arg == 'IPCA':
            card_texts.append("{:.2f}%".format(ipca_return))
        elif arg == 'BOVA11':
            card_texts.append("{:.2f}%".format(bova11_return))
        
    for i in range(1,17):

        if i in [1, 2, 3, 4, 5, 9, 10, 11, 12, 15, 16]:

            if stat[i] > 0:
                formatted_stats.append('text-success')
            elif stat[i] < 0:
                formatted_stats.append('text-danger')
        else:
            formatted_stats.append('text-muted')

    if strategy_return > cdi_return and strategy_return > ipca_return and strategy_return > bova11_return:
        formatted_stats.append('text-success')
    else:
        formatted_stats.append('text-muted')

    if cdi_return > strategy_return and cdi_return > ipca_return and cdi_return > bova11_return:
        formatted_stats.append('text-success')
    else:
        formatted_stats.append('text-muted')

    if ipca_return > strategy_return and ipca_return > cdi_return and ipca_return > bova11_return:
        formatted_stats.append('text-success')
    else:
        formatted_stats.append('text-muted')

    if bova11_return > strategy_return and bova11_return > cdi_return and bova11_return > ipca_return:
        formatted_stats.append('text-success')
    else:
        formatted_stats.append('text-muted')

    #Unificar as duas listas
    outputs = card_texts + formatted_stats
            
    return outputs


if __name__ == '__main__':
    app.run_server()

    # return f'{stat[0]:.2f}%', f'R$ {stat[1]:.2f}', f'R$ {stat[2]:.2f}', f'R$ {stat[3]:.2f}', f'{stat[4]:.1f}%', f'{stat[5]}', f'{stat[6]}', f'{stat[7]}', f'{stat[8]:.2f}x', f'{stat[9]:.2f}%', f'R$ {stat[10]:.2f}', f'R$ {stat[11]:.2f}', f'{stat[12]}', f'{stat[13]}', f'{stat[14]:.2f}', f'R$ {stat[15]:.2f}'
