from dash import html
import datetime
import dash_bootstrap_components as dbc

class Header:

    def __init__(self, strategy_info, start_date, end_date):
        self.strategy_info = strategy_info
        self.start_date = start_date
        self.end_date = end_date
        
    def create_header(self):
        return html.Div(
            className="print-background",
            style={
                "backgroundColor": "#171E27",
                "height": "100vh",
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "flexDirection": "column",
                "position": "relative",  # Necessário para posicionar a logo
            },
            children=[
                html.Img(
                    src="/assets/logo_ontick.png",
                    style={
                        "position": "absolute",
                        "top": "50%",
                        "left": "20%",
                        "transform": "translate(-50%, -50%) rotate(-90deg)",  # Rotaciona a imagem
                        "opacity": "0.1",  # Define a transparência
                        "height": "20%",  # Ajusta a altura da imagem
                    },
                ),
                html.Div(
                    children=[
                        html.H1(
                            "{}".format(self.strategy_info[0]), className='header-title',
                            #"Carta do Analista", className='header-title',

                        ),
                        html.H3(
                            "{} - {}".format(self.start_date, self.end_date), className='header-subtitle',
                        ),
                        html.Div(
                            "Atualizado em: {}".format(datetime.datetime.now().strftime("%d/%m/%Y")),
                            style={
                                "color": "#888888",
                                "fontSize": "0.9rem",
                                "position": "absolute",
                                "bottom": "10px",
                                "right": "10px",
                            },
                        ),
                    ],
                    style={"textAlign": "center"}
                ),
            ],
        )

    def create_final_page(self,):
        return html.Div(
            className="print-background",
            style={
                "backgroundColor": "#192231",
                "height": "100vh",
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "space-between",
                "padding": "40px",
                "position": "relative",  # Necessário para posicionar a logo
            },
            children=[
                html.Div(
                    children=[
                        html.Img(
                            src="/assets/logo_ontick.png",
                            style={
                                "position": "absolute",
                                "top": "50%",  # Centraliza verticalmente na metade da página
                                "left": "50%",
                                "transform": "translate(-50%, -50%)",
                                # "opacity": "0.1",  # Define a transparência
                                # "height": "40vh",  # Ajusta a altura da imagem
                            },
                        ),
                    ],
                    style={"textAlign": "center", "flex": "1"}
                ),
                html.Div(
                    children=[
                        html.H3(
                            "Disclaimer",
                            style={
                                "color": "white",
                                "marginBottom": "0.5rem",
                                "borderBottom": "2px solid #00bdaa",
                                "paddingBottom": "0.5rem",
                            },
                        ),
                        html.P(
                            [

                                html.Span("Investimentos e estratégias de investimento apresentam riscos potenciais e retornos. "),
                                html.Span("Desempenhos passados não são indicativos de resultados futuros. "),
                                html.Span("Nós não garantimos qualquer resultado específico ou lucro. "),
                                html.Span("Você deve estar ciente dos riscos e estar disposto a aceitá-los para investir nos mercados. "),
                                html.Span("Qualquer decisão de investimento que você tome deve ser baseada em sua própria diligência e consideração de suas circunstâncias pessoais, incluindo, "),
                                html.Span("mas não se limitando a, sua tolerância ao risco, situação financeira e objetivos de investimento. "),
                                html.Span("Nós não nos responsabilizamos por quaisquer perdas que você possa sofrer como resultado do uso das informações, dados ou serviços da plataforma. "),
                                html.Span("Ao utilizar nosso site e nossos serviços, você concorda com este aviso de isenção de responsabilidade e assume total responsabilidade por suas decisões e ações.​"),
                            ],
                            style={
                                "color": "white",
                                "lineHeight": "1.6",
                                "marginTop": "20px",
                                "fontSize": "0.9rem",
                            }
                        ),
                    ],
                    style={
                        "marginBottom": "20px",  # Espaço entre o disclaimer e o footer
                    }
                ),
                html.Div(
                    html.Img(src="/assets/ontick_footer2.png"),
                    style={
                        "width": "100%",
                        "display": "block",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "color": "white",
                        "borderTop": "1px solid #00bdaa",
                        "paddingTop": "20px",
                    },
                ),
            ],
        )