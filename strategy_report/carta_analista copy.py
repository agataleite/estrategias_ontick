import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from src.StrategyDetails import StrategyDetails
from src.HeaderCartaGestor import Header
import plotly.graph_objects as go

# Inicializa o aplicativo Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,
                                                "/assets/style.css"])


#Input do python para receber qual o strategy_id do portfólio
strategy_id_1 = 1194
strategy_id_2 = 1193
strategy_id_3 = 1219

# strategy_id = int(input("Digite o strategy_id: "))

# strategy_id = 155
strategy_1 = StrategyDetails(strategy_id_1)
strategy_2 = StrategyDetails(strategy_id_2)
strategy_3 = StrategyDetails(strategy_id_3)

strategy_info_1 = strategy_1.get_strategy_info()
strategy_info_2 = strategy_2.get_strategy_info()
strategy_info_3 = strategy_3.get_strategy_info()


fig_capital_curve_1, fig_monthly_returns_1 = strategy_1.create_curve_capital_and_monthly_returns()
fig_capital_curve_2, fig_monthly_returns_2 = strategy_2.create_curve_capital_and_monthly_returns()
fig_capital_curve_3, fig_monthly_returns_3 = strategy_3.create_curve_capital_and_monthly_returns()


# Criando uma figura vazia
fig_combined = go.Figure()

# Adicionando os dados de cada curva de capital ao gráfico combinado
for fig in [fig_capital_curve_1, fig_capital_curve_2, fig_capital_curve_3]:
    for trace in fig.data:  # Extraindo cada linha do gráfico original
        fig_combined.add_trace(trace)

# Aplicando o layout do primeiro gráfico (ou outro de sua escolha)
fig_combined.update_layout(fig_capital_curve_1.layout)


strategy_details_1 = strategy_1.create_strategy_details()
strategy_details_2 = strategy_2.create_strategy_details()
strategy_details_3 = strategy_3.create_strategy_details()


# fig_strategy_performance, strategy_return, cdi_return, ipca_return, bova11_return = strategy.create_strategy_performance()
stat = strategy_1.create_strategy_statistics()
header_class = Header(strategy_info_1, strategy_1.get_initial_end_date()[0], strategy_1.get_initial_end_date()[1])


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

        html.Hr(style={'border-top': '6px solid #EAEBED'}),

    ]),

    html.Div([
            #Criar uma área para texto
            dbc.Row([
                html.Div(
                    children=[
                        html.H2('Mês de Janeiro/25', style={'padding': '0 50px'}, className='title'),
                        html.P(
                            "Iniciamos o ano de 2025 com um mês marcado por forte tendência no mercado acionário brasileiro. O Ibovespa registrou uma valorização de +4,86%, impulsionado pelo otimismo dos investidores e fatores macroeconômicos favoráveis. No mercado de câmbio, o contrato futuro de dólar (DOLG2025) sofreu uma desvalorização expressiva de -6,26%, refletindo o fluxo de capital para ativos de risco e a valorização do real. Em um cenário predominantemente direcional, nossas estratégias automatizadas apresentaram bons desempenhos, com destaque para três modelos que melhor se adaptaram a este tipo de mercado:",
                            className='text_auto_height'
                        ),
                        html.Hr(style={'border-top': '2px solid #EAEBED'}),


                        html.H4('Two White Soldiers - V2', style={'padding': '0 50px'}, className='title'),

                        html.P(
                            "A estratégia registrou uma valorização de 40,95% em termos de juros compostos em relação ao mês anterior, resultando em um lucro líquido de R$ 1.127,00 com 2 contratos. Considerando o capital recomendado, a valorização foi de 28,18%.",
                            className='text_auto_height'
                        ),

                        
                        #html.H6('Retornos mensais', style={'padding': '0 50px'}, className='title'),
                            dcc.Graph(
                                id='monthly-returns-1',
                                figure=fig_monthly_returns_1,
                                className='graph'
                            ),
        

                        html.Hr(style={'border-top': '2px solid #EAEBED'}),

                        

                        html.H4('Two White Soldiers M10', style={'padding': '0 50px'}, className='title'),

                        html.P(
                            "Em juros compostos, a estratégia apresentou uma valorização de 20,94% no último mês, totalizando um lucro líquido de R$ 1.010,00 com 2 contratos. Em relação ao capital recomendado, a valorização foi de 25,25%.",
                            className='text_auto_height'
                        ),

                        #html.H6('Retornos mensais', style={'padding': '0 50px'}, className='title'),
                            dcc.Graph(
                                id='monthly-returns-2',
                                figure=fig_monthly_returns_2,
                                className='graph'
                            ),

                        html.Hr(style={'border-top': '1px solid #EAEBED'}),

                        #Quebra de página
                        html.Div(className="page-break"),

                        html.Hr(style={'border-top': '8px solid #EAEBED'}),

                        html.H4('IFR + Afastamento Media', style={'padding': '0 50px'}, className='title'),

                        html.P(
                            "A estratégia obteve uma valorização de 12,58% em juros compostos no período, com um lucro líquido de R$ 418,00 operando com 1 contrato. Com base no capital recomendado, a valorização foi de 13,93%.",
                            className='text_auto_height'
                        ),

                        #html.H6('Retornos mensais', style={'padding': '0 50px'}, className='title'),
                            dcc.Graph(
                                id='monthly-returns-3',
                                figure=fig_monthly_returns_3,
                                className='graph'
                            ),

                        html.Hr(style={'border-top': '0.5px solid #EAEBED'}),

                        html.P(
                            "Janeiro foi um mês que exemplificou a importância de contar com estratégias diversificadas e bem calibradas para diferentes condições de mercado. Acreditamos que, com um portfólio robusto de modelos quantitativos, conseguimos explorar as melhores oportunidades, minimizando riscos e maximizando retornos ao longo do tempo. ",
                            className='text_auto_height'
                        ),

                        html.Hr(style={'border-top': '0.5px solid #EAEBED'}),


                    ],
                ),
            ]),

            html.Hr(style={'border-top': '6px solid #EAEBED'}),

            #Adicionar 2 imagens que estão em assets
            dbc.Row([
                
                html.Div(
                    children=[
                        html.H2('Estatísticas Paper Trade', style={'padding': '0 50px'}, className='title'),
                        html.P(
                            "A análise do paper trade das estratégias mostra como cada modelo vem se comportando ao longo do tempo:",                            
                            className='text_auto_height'
                        ),
                        
                        

                        html.Hr(style={'border-top': '1px solid #EAEBED'}),


                        html.H4('Two White Soldiers - V2', style={'padding': '0 50px'}, className='title'),

                        html.P(
                            "Apesar do bom desempenho em janeiro, a estratégia ainda apresenta um saldo negativo no paper trade, com 1,23%, um resultado líquido de R$ 49,00, e um máximo drawdown de 38,67%. A taxa de acerto da estratégia é de 53,1%, com um fator de lucro de 0,99x, utilizando 2 contratos. Veja no gráfico de curva de capital abaixo como a estratégia tem se comportado ao longo do tempo. ",
                            className='text_auto_height'
                        ),
                        dbc.Row([
                        # html.H2('Curva de Capital', style={'padding': '0 50px'}, className='title'),
                            #html.H6('Curva de Capital ', style={'padding': '0 50px'}, className='title'),

                            dcc.Graph(     
                                id='capital-curve-1',
                                figure=fig_capital_curve_1,
                                className='graph'
                            ),
                        ]),

                        # #Quebra de página
                        html.Div(className="page-break"),

                        html.Hr(style={'border-top': '7px solid #EAEBED'}),

                        html.H4('Two White Soldiers M10', style={'padding': '0 50px'}, className='title'),

                        html.P(
                            "O excelente resultado em janeiro elevou ainda mais a rentabilidade da estratégia, que agora acumula uma valorização de 45,85%, com um resultado líquido de R$ 1.834,00, e um máximo drawdown de 35,14%. A taxa de acerto é de 55,1%, com um fator de lucro de 1,15x, utilizando 2 contratos. Consulte o gráfico de curva de capital abaixo para visualizar a progressão da rentabilidade da estratégia.",
                            className='text_auto_height'
                        ),

                        dbc.Row([
                        # html.H2('Curva de Capital', style={'padding': '0 50px'}, className='title'),
                            #html.H6('Curva de Capital ', style={'padding': '0 50px'}, className='title'),

                            dcc.Graph(     
                                id='capital-curve-2',
                                figure=fig_capital_curve_2,
                                className='graph'
                            ),
                        ]),

                        html.Hr(style={'border-top': '1px solid #EAEBED'}),

                        html.H4('IFR + Afastamento Media', style={'padding': '0 50px'}, className='title'),

                        html.P(
                            "Assim como a M10, esta estratégia também teve um incremento positivo na rentabilidade, alcançando 24,67%, com um resultado líquido de R$ 740,00, e um máximo drawdown de 29,72%. A taxa de acerto é de 49,38%, com um fator de lucro de 1,15x, utilizando 1 contrato. O gráfico de curva de capital abaixo ilustra a evolução da rentabilidade dessa estratégia, mostrando como ela tem se comportado ao longo do tempo.",
                            className='text_auto_height'
                        ),

                        dbc.Row([
                        # html.H2('Curva de Capital', style={'padding': '0 50px'}, className='title'),
                            #html.H6('Curva de Capital ', style={'padding': '0 50px'}, className='title'),

                            dcc.Graph(     
                                id='capital-curve-3',
                                figure=fig_capital_curve_3,
                                className='graph'
                            ),
                        ]),

                        
                        


                    ],
                ),

                #html.Hr(style={'border-top': '1px solid #EAEBED'}),

                # dbc.Col([
                #     html.H2('Outubro/24', className='text-image'),
                #     html.Img(src='/assets/ontick_tws.png', className='image')
                # ]),
                # dbc.Col([
                #     html.H2('Paper Trade', className='text-image'),
                #     html.Img(src='/assets/ontick_tws_com_outubro.png', className='image')
                # ]),
            ]),

            html.Hr(style={'border-top': '1px solid #EAEBED'}),

            html.Div(
                children=[
                    html.H2('Próximos cenários', style={'padding': '0 50px'}, className='title'),
                     html.P(
                            "Se o mercado continuar apresentando tendência, as estratégias citadas neste relatório devem continuar se beneficiando, independentemente da direção – seja de alta ou de baixa. Essas estratégias têm como característica principal a capacidade de capturar movimentos direcionais e extrair oportunidades de lucro em mercados com forte tendência. ",                            
                            className='text_auto_height'
                        ),
                        html.P(
                            "Por outro lado, é essencial reforçar a importância da diversificação de estratégias. Para um portfólio mais equilibrado, recomendamos também a utilização de estratégias que operam bem em mercados consolidados, garantindo maior resiliência e consistência nos resultados ao longo do tempo.",
                            className='text_auto_height'
                        ),
                ],
            ),
    ]),

    # #Quebra de página
    # html.Div(className="page-break"),

    # html.Div([
        
    #     html.Hr(style={'border-top': '1px solid #EAEBED'}),

    #     dbc.Row([
    #             # html.H2('Curva de Capital', style={'padding': '0 50px'}, className='title'),
    #             html.H4('Curva de Capital Two White Soldiers - V2', style={'padding': '0 50px'}, className='title'),

    #         dcc.Graph(     
    #             id='capital-curve-1',
    #             figure=fig_capital_curve_1,
    #             className='graph',
    #             style={'backgroundColor': '#f0f0f0'}  # Alterando a cor de fundo do gráfico

    #         ),
    #     ]),

    #     html.Hr(style={'border-top': '1px solid #EAEBED'}),

    #      dbc.Row([
    #             # html.H2('Curva de Capital', style={'padding': '0 50px'}, className='title'),
    #             html.H4('Curva de Capital Two White Soldiers M10', style={'padding': '0 50px'}, className='title'),
    #         dcc.Graph(     
    #             id='capital-curve-2',
    #             figure=fig_capital_curve_2,
    #             className='graph'
    #         ),
    #     ]),

    #     html.Hr(style={'border-top': '1px solid #EAEBED'}),

    #      dbc.Row([
    #             # html.H2('Curva de Capital', style={'padding': '0 50px'}, className='title'),
    #             html.H4('Curva de Capital IFR + Afastamento Media', style={'padding': '0 50px'}, className='title'),
    #         dcc.Graph(     
    #             id='capital-curve-3',
    #             figure=fig_capital_curve_3,
    #             className='graph'
    #         ),
    #     ]),
        # # Criando uma figura vazia
        # fig_combined = go.Figure()

        # # Adicionando os dados de cada curva de capital ao gráfico combinado
        # for fig in [fig_capital_curve_1, fig_capital_curve_2, fig_capital_curve_3]:
        #     for trace in fig.data:  # Extraindo cada linha do gráfico original
        #         fig_combined.add_trace(trace)

        # # Aplicando o layout do primeiro gráfico (ou outro de sua escolha)
        # fig_combined.update_layout(fig_capital_curve_1.layout)

        # dbc.Row([
        #         # html.H2('Curva de Capital', style={'padding': '0 50px'}, className='title'),
        #         html.H4('Curva de Capital das três estratégias', style={'padding': '0 50px'}, className='title'),
        #     dcc.Graph(     
        #         id='capital-curve-4',
        #         figure=fig_combined,
        #         className='graph'
        #     ),
        # ]),
        
 

        

        html.Hr(style={'border-top': '1px solid #EAEBED'}),
    # ]),

        # # Criando uma figura vazia
        # fig_combined = go.Figure()

        # # Adicionando os dados de cada curva de capital ao gráfico combinado
        # for fig in [fig_capital_curve_1, fig_capital_curve_2, fig_capital_curve_3]:
        #     for trace in fig.data:  # Extraindo cada linha do gráfico original
        #         fig_combined.add_trace(trace)

        # # Aplicando o layout do primeiro gráfico (ou outro de sua escolha)
        # fig_combined.update_layout(fig_capital_curve_1.layout)

        # dbc.Row([
        #         # html.H2('Curva de Capital', style={'padding': '0 50px'}, className='title'),
        #         html.H4('Curva de Capital das três estratégias', style={'padding': '0 50px'}, className='title'),
        #     dcc.Graph(     
        #         id='capital-curve-combined',
        #         figure=fig_combined,
        #         className='graph'
        #     ),
        # ]),
    
    
        
    

        

    # html.Div([
        
    #     dbc.Row([
    #             html.H2('Diversificação', style={'padding': '0 50px'}, className='title'),
    #             html.P(
    #                 "Contar com uma única estratégia pode aumentar os riscos em condições de mercado adversas. Diversificar permite equilibrar o desempenho, pois quando uma estratégia enfrenta perdas, outras podem compensar. Isso ajuda a reduzir a volatilidade dos resultados, proteger o capital e aproveitar diferentes movimentos de mercado, como tendências e reversões. Diversificar estratégias, portanto, é essencial para uma gestão de risco eficaz e para garantir maior estabilidade nos retornos ao longo do tempo. Para ilustrar essa prática, trouxemos aqui duas estratégias que poderiam ser utilizadas em conjunto com a Two White Soldiers M10, diversificando as operações e reduzindo o impacto do drawdown.",
    #                 className='text_auto_height'
    #             ),
    #             html.Hr(style={'border-top': '1px solid #EAEBED'}),

    #             dbc.Col([
    #                 html.H2('Keltner Five', className='text-image'),
    #                 html.Img(src='/assets/keltner_five.png', className='image')
    #             ]),
    #             dbc.Col([
    #                 html.H2('HMA BullBear', className='text-image'),
    #                 html.Img(src='/assets/hma_bullbear.png', className='image')
    #             ]),
    #     ]),

    #     html.Hr(style={'border-top': '1px solid #EAEBED'}),
    # ]),



    #Quebra de página
    html.Div(className="page-break"),
    
    html.Div(final_page)

], fluid=True, style={'padding': '0'})


if __name__ == '__main__':
    app.run_server()

    # return f'{stat[0]:.2f}%', f'R$ {stat[1]:.2f}', f'R$ {stat[2]:.2f}', f'R$ {stat[3]:.2f}', f'{stat[4]:.1f}%', f'{stat[5]}', f'{stat[6]}', f'{stat[7]}', f'{stat[8]:.2f}x', f'{stat[9]:.2f}%', f'R$ {stat[10]:.2f}', f'R$ {stat[11]:.2f}', f'{stat[12]}', f'{stat[13]}', f'{stat[14]:.2f}', f'R$ {stat[15]:.2f}'
