import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from src.StrategyDetails import StrategyDetails
from src.HeaderCartaGestor import Header

# Inicializa o aplicativo Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,
                                                "/assets/style.css"])


#Input do python para receber qual o strategy_id do portfólio
strategy_id = 1193
# strategy_id = int(input("Digite o strategy_id: "))

# strategy_id = 155
strategy = StrategyDetails(strategy_id)

strategy_info = strategy.get_strategy_info()
fig_capital_curve, fig_monthly_returns = strategy.create_curve_capital_and_monthly_returns()
strategy_details = strategy.create_strategy_details()
# fig_strategy_performance, strategy_return, cdi_return, ipca_return, bova11_return = strategy.create_strategy_performance()
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

    ]),

    html.Div([
            #Criar uma área para texto
            dbc.Row([
                html.Div(
                    children=[
                        html.H2('Mês de Outubro/24', style={'padding': '0 50px'}, className='title'),
                        html.P(
                            "A estratégia Two White Soldiers M10 interrompeu uma sequência de seis meses consecutivos de ganhos, encerrando o mês de outubro com um desempenho negativo de -24,51%. O período foi caracterizado por uma redução na volatilidade, com o Ibovespa recuando -1,60%, enquanto o dólar avançou +5,69% frente ao real, revelando uma discrepância nos níveis de volatilidade entre os ativos. A Two White Soldiers M10 é uma estratégia seguidora de tendência. Em outubro, no entanto, o mercado apresentou um padrão consolidado, favorecendo estratégias de reversão e consolidação em detrimento de estratégias trend-following. Além disso, o alvo da estratégia, definido em 900 pontos, não foi alcançado em nenhuma operação ao longo do mês. A estratégia inclui ainda uma realização parcial e um ponto de breakeven quando o mercado avança 350 pontos a favor, porém, em outubro, esse patamar raramente foi atingido, o que resultou em uma série de stops consecutivos.",
                            className='text_auto_height'
                        ),
                    ],
                ),
            ]),

            # html.Hr(style={'border-top': '1px solid #EAEBED'}),

            #Adicionar 2 imagens que estão em assets
            dbc.Row([
                
                html.Div(
                    children=[
                        html.H2('Estatísticas Paper Trade', style={'padding': '0 50px'}, className='title'),
                        html.P(
                            "Com base no capital mínimo recomendado de R$4.000,00, o resultado da estratégia no mês de outubro foi de -R$1.773,00, equivalente a uma desvalorização de -44,33%. A taxa de acerto fechou em 33,33%, com um fator de lucro de 0,34. Esse desempenho negativo é considerado atípico, dado que a estratégia normalmente apresenta uma taxa média de acerto de aproximadamente 51% e um fator de lucro em torno de 1,5. ",                            
                            className='text_auto_height'
                        ),
                        html.P(
                            "Desde o início do paper trade, em abril de 2024, o retorno financeiro acumulado é de R$1.963,00, refletindo uma valorização de +49,08% sobre o capital inicial. Nas imagens a seguir, é possível observar o desempenho da Two White Soldiers M10 tanto no mês de outubro de 2024 quanto desde o início do paper trade. Embora o resultado mensal tenha sido negativo, a estratégia ainda apresenta um saldo positivo em seu histórico.",
                            className='text_auto_height'
                        )
                    ],
                ),

                html.Hr(style={'border-top': '1px solid #EAEBED'}),

                dbc.Col([
                    html.H2('Outubro/24', className='text-image'),
                    html.Img(src='/assets/ontick_tws.png', className='image')
                ]),
                dbc.Col([
                    html.H2('Paper Trade', className='text-image'),
                    html.Img(src='/assets/ontick_tws_com_outubro.png', className='image')
                ]),
            ]),

            html.Hr(style={'border-top': '1px solid #EAEBED'}),

            html.Div(
                children=[
                    html.H2('Próximos cenários', style={'padding': '0 50px'}, className='title'),
                    html.P(
                        "Após um mês de outubro desafiador, espera-se que novembro seja marcado por uma volatilidade acentuada, impulsionada pelo fortalecimento do dólar e pelo impacto das eleições americanas, eventos que tradicionalmente aumentam a oscilação nos mercados. A estratégia Two White Soldiers M10 pode se beneficiar desse cenário ao capturar movimentos de tendência, especialmente considerando que está atualmente em um período de drawdown, o que pode representar um ponto favorável para recuperação. Esse comportamento pode ser observado na curva de capital abaixo.",
                        className='text_auto_height'
                    ),
                ],
            ),
    ]),

    #Quebra de página
    html.Div(className="page-break"),

    html.Div([
        
        html.Hr(style={'border-top': '1px solid #EAEBED'}),

        dbc.Row([
                # html.H2('Curva de Capital', style={'padding': '0 50px'}, className='title'),
            dcc.Graph(     
                id='capital-curve',
                figure=fig_capital_curve,
                className='graph'
            ),
        ]),

        html.Hr(style={'border-top': '1px solid #EAEBED'}),
    ]),
        

    html.Div([
        
        dbc.Row([
                html.H2('Diversificação', style={'padding': '0 50px'}, className='title'),
                html.P(
                    "Contar com uma única estratégia pode aumentar os riscos em condições de mercado adversas. Diversificar permite equilibrar o desempenho, pois quando uma estratégia enfrenta perdas, outras podem compensar. Isso ajuda a reduzir a volatilidade dos resultados, proteger o capital e aproveitar diferentes movimentos de mercado, como tendências e reversões. Diversificar estratégias, portanto, é essencial para uma gestão de risco eficaz e para garantir maior estabilidade nos retornos ao longo do tempo. Para ilustrar essa prática, trouxemos aqui duas estratégias que poderiam ser utilizadas em conjunto com a Two White Soldiers M10, diversificando as operações e reduzindo o impacto do drawdown.",
                    className='text_auto_height'
                ),
                html.Hr(style={'border-top': '1px solid #EAEBED'}),

                dbc.Col([
                    html.H2('Keltner Five', className='text-image'),
                    html.Img(src='/assets/keltner_five.png', className='image')
                ]),
                dbc.Col([
                    html.H2('HMA BullBear', className='text-image'),
                    html.Img(src='/assets/hma_bullbear.png', className='image')
                ]),
        ]),

        html.Hr(style={'border-top': '1px solid #EAEBED'}),
    ]),


    #Quebra de página
    html.Div(className="page-break"),
    
    html.Div(final_page)

], fluid=True, style={'padding': '0'})


if __name__ == '__main__':
    app.run_server(debug=True)

    # return f'{stat[0]:.2f}%', f'R$ {stat[1]:.2f}', f'R$ {stat[2]:.2f}', f'R$ {stat[3]:.2f}', f'{stat[4]:.1f}%', f'{stat[5]}', f'{stat[6]}', f'{stat[7]}', f'{stat[8]:.2f}x', f'{stat[9]:.2f}%', f'R$ {stat[10]:.2f}', f'R$ {stat[11]:.2f}', f'{stat[12]}', f'{stat[13]}', f'{stat[14]:.2f}', f'R$ {stat[15]:.2f}'
