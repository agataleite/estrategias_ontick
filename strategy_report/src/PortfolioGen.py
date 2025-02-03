import pandas as pd
import plotly.graph_objs as go
from sshtunnel import SSHTunnelForwarder, BaseSSHTunnelForwarderError
import pymysql
import time
from dotenv import load_dotenv
import json
import os
import dash_bootstrap_components as dbc
import yfinance as yf 
from dash import dash_table
import datetime

load_dotenv()
ssh_host = os.getenv("ssh_host")
ssh_port = int(os.getenv("ssh_port"))
ssh_user = os.getenv("ssh_user")
ssh_key = os.getenv("ssh_key")

db_host = os.getenv("db_host")
db_port = int(os.getenv("db_port"))
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_name = os.getenv("db_name")

class StrategyDetails:

    def __init__(self, strategy_id):
        self.strategy_id = strategy_id
    
    def get_strategy_info(self):
        #Criar conexão SSH  
        with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_private_key=ssh_key,
            remote_bind_address=(db_host, db_port)
        ) as tunnel:
            try:
                #Conectar ao banco de dados
                connection = pymysql.connect(
                    host='127.0.0.1',
                    user=db_user,
                    password=db_password,
                    db=db_name,
                    port=tunnel.local_bind_port
                )
                #Executar a consulta SQL
                with connection.cursor() as cursor:

                    #Pegar as posições do investimento
                    sql = f"""
                        SELECT ts.strategy_id, ts.strategy_name, ts.strategy_risk, ts.strategy_style, ts.strategy_tier, ts.strategy_symbol, ts.strategy_timeframe, ts.min_capital, ts.min_capital, ts.max_daily_loss,
                        ts.strategy_params, tp.product_owner, tp.product_description, tp.product_strategy, tp.product_datetime
                        FROM tb_strategies ts 
                        INNER JOIN tb_products tp ON ts.product_id = tp.product_id 
                        where strategy_id = {self.strategy_id};
                        """

                    cursor.execute(sql)
                    result = cursor.fetchall()
                    #Passar para um DataFrame

                    self.strategy_name = result[0][1]
                    self.strategy_risk = result[0][2]
                    self.strategy_style = result[0][3].replace("_", " ")
                    self.strategy_tier = result[0][4]
                    self.strategy_symbol = result[0][5]
                    self.strategy_timeframe = result[0][6]
                    self.min_capital = result[0][7]
                    self.max_daily_loss = result[0][9]
                    self.strategy_params = json.loads(result[0][10])
                    self.product_owner = result[0][11]
                    self.product_description = json.loads(result[0][12])['description']
                    self.product_strategy = result[0][13]
                    self.product_datetime = result[0][14]

                    return self.strategy_name, self.strategy_risk, self.strategy_style, self.strategy_tier, self.strategy_symbol, self.strategy_timeframe, self.min_capital, self.max_daily_loss, self.strategy_params, self.product_owner, self.product_description, self.product_strategy, self.product_datetime
                    
            except BaseSSHTunnelForwarderError as e:
                print(f"Erro ao criar o túnel SSH: {e}")
            except pymysql.MySQLError as e:
                print(f"Erro ao conectar ao banco de dados: {e}")
            finally:
                # Fechando a conexão
                connection.close()
                    
    def track_record_strategy(self):

        #Criar conexão SSH  
        with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_private_key=ssh_key,
            remote_bind_address=(db_host, db_port)
        ) as tunnel:
            try:
                #Conectar ao banco de dados
                connection = pymysql.connect(
                    host='127.0.0.1',
                    user=db_user,
                    password=db_password,
                    db=db_name,
                    port=tunnel.local_bind_port
                )
                #Executar a consulta SQL
                with connection.cursor() as cursor:
                    
                    #Pegar as posições do investimento
                    sql = f"""
                        SELECT position_time_current, position_type, investment_id, position_profit from tb_positions tp 
                        where investment_id in (SELECT investment_id from tb_track_record ttr where tr_id IN (
                        SELECT track_record_id from tb_strategies ts where strategy_id = {self.strategy_id}));
                        """
                                        
                    cursor.execute(sql)
                    result = pd.DataFrame(cursor.fetchall(), columns=['datetime', 'position_type', 'investment_id', 'position_profit'])
                    
                    # self.min_capital = 4000

                    len_operacoes_compra = len(result[result['position_type'] == 'BUY'])
                    len_operacoes_venda = len(result[result['position_type'] == 'SELL'])
                    percent_operacoes_compra = round(len_operacoes_compra / len(result),1)
                    percent_operacoes_venda = round(len_operacoes_venda / len(result),1)

                    #Calcular o drawdown
                    result = result.sort_values(by='datetime').reset_index(drop=True)                                    
                    result = result.drop(columns=['position_type', 'investment_id'])
                    result.set_index('datetime', inplace=True)                    
                    result = result.resample('D').sum()
                    result['result'] = result['position_profit'].cumsum() + self.min_capital

                    resultado_percentual = (result['result'].iloc[-1] - self.min_capital) / self.min_capital * 100
                    resultado_bruto = result['result'].iloc[-1] - self.min_capital
                    lucro_total = result[result['position_profit'] >= 0]['position_profit'].sum()
                    perda_total = result[result['position_profit'] < 0]['position_profit'].sum()
                    taxa_de_acerto = len(result[result['position_profit'] > 0]) / result[result['position_profit'] != 0]['position_profit'].count() * 100
                    quantidade_operacoes = len(result)
                    operacoes_com_ganho = round(taxa_de_acerto / 100 * quantidade_operacoes)
                    operacoes_com_perda = quantidade_operacoes - operacoes_com_ganho
                    fator_de_lucro = lucro_total / abs(perda_total)
                    lucro_medio = result[result['position_profit'] > 0]['position_profit'].mean()
                    prejuizo_medio = result[result['position_profit'] < 0]['position_profit'].mean()
                    quantidade_operacoes_compra = round(quantidade_operacoes * percent_operacoes_compra)
                    quantidade_operacoes_venda = round(quantidade_operacoes * percent_operacoes_venda)                
                    rrr_medio = lucro_medio / abs(prejuizo_medio)
                    perda_maxima_historica = result['position_profit'].min()

                    #Adicionar uma linha no index 0 no dia anterior ao primeiro dia e adicionar o valor mínimo
                    result.loc[result.index[0] - pd.Timedelta(days=1)] = self.min_capital
                    result = result.sort_index()

                    #Calcular o drawdown
                    result['max_result'] = result['result'].cummax()
                    result['drawdown'] = result['result'] - result['max_result']
                    max_drawdown = result['drawdown'].min()
                    drawdown_pct = max_drawdown / result['max_result'].max() * 100

                    #Pegar a data inicial
                    self.data_inicial = result['result'].index[0].strftime("%d/%m/%Y")
                    self.data_final = result['result'].index[-1].strftime("%d/%m/%Y")


                    return result['result'], resultado_percentual, resultado_bruto, lucro_total, perda_total, taxa_de_acerto, quantidade_operacoes, operacoes_com_ganho, operacoes_com_perda, fator_de_lucro, drawdown_pct, prejuizo_medio, lucro_medio, quantidade_operacoes_compra, quantidade_operacoes_venda, rrr_medio, perda_maxima_historica
                                                
            except BaseSSHTunnelForwarderError as e:
                print(f"Erro ao criar o túnel SSH: {e}")
            except pymysql.MySQLError as e:
                print(f"Erro ao conectar ao banco de dados: {e}")
            finally:
                # Fechando a conexão
                connection.close()

    def monthly_returns(self,data):
        try:

            df = data.copy()

            # Calcular os retornos diários
            daily_returns = df.pct_change()

            # Agrupar por mês e calcular o retorno acumulado para cada mês
            monthly_returns = daily_returns.resample('M').apply(lambda x: (1 + x).prod() - 1)

            # Converter para porcentagem
            monthly_returns = monthly_returns * 100

            # Criar DataFrame de retornos mensais
            returns_df = pd.DataFrame(monthly_returns, columns=["result"])
            returns_df.index = pd.to_datetime(returns_df.index)

            # Adicionar colunas de ano e mês
            returns_df["Year"] = returns_df.index.strftime("%Y")
            returns_df["Month"] = returns_df.index.strftime("%b")

            # Criar tabela pivot
            returns_pivot = returns_df.pivot(index="Year", columns="Month", values="result").fillna(0)

            # Lidar com meses ausentes
            for month in [
                "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
            ]:
                if month not in returns_pivot.columns:
                    returns_pivot.loc[:, month] = 0

            # Ordenar colunas por mês
            returns_pivot = returns_pivot[
                ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            ]

            eoy = True

            if eoy:
                eoy_returns = daily_returns.resample('A').apply(lambda x: (1 + x).prod() - 1) * 100
                returns_pivot["EOY"] = eoy_returns.values

            returns_pivot.columns = map(lambda x: str(x).upper(), returns_pivot.columns)
            returns_pivot.index.name = None

            # Converter os valores para float
            returns_pivot = returns_pivot.astype(float)

            #Renomear as colunas
            returns_pivot.columns = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez", "Retorno Anual"]

            return returns_pivot

            #Gravar em um JSON
            # returns_pivot.to_json("./json_file/retornos_anuais.json", orient="index")


        except Exception as e:
            print("Error na função monthly_returns: ", e)        

    def create_strategy_details(self):


        strategy_info = self.get_strategy_info()

        data = [
            {"Característica": "Ativo", "Valor": strategy_info[4]},
            {"Característica": "Estilo", "Valor": strategy_info[2]},
            {"Característica": "Risco", "Valor": strategy_info[1]},
            {"Característica": "Plano", "Valor": strategy_info[3]},
            {"Característica": "Timeframe", "Valor": strategy_info[5]},
            {"Característica": "Capital mínimo", "Valor": "R$ {}".format(strategy_info[6])},
            {"Característica": "Perda máxima diária", "Valor": "R$ {}".format(strategy_info[7])},
            {"Característica": "Data de criação da estratégia", "Valor": "{}".format(strategy_info[12].strftime("%d/%m/%Y"))},
            {"Característica": "Desenvolvedor", "Valor": strategy_info[9]},
        ]

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

    def create_strategy_performance(self):

        self.generate_benchmark()

        data = self.track_record_strategy()[0]

        #Retorno acumulado da estratégia
        data = ((data.astype(float).pct_change() + 1).cumprod() - 1) * 100
        data.fillna(0, inplace=True)

        #Ler o arquivo JSON e passar para um dataframe
        cdi = pd.read_json("./data/cdi.json", orient="index")
        cdi.index = pd.to_datetime(cdi.index)

        #Ler o arquivo JSON e passar para um dataframe
        ipca = pd.read_json("./data/ipca.json", orient="index")
        ipca.index = pd.to_datetime(ipca.index)

        #Ler o arquivo JSON e passar para um dataframe
        bova11 = pd.read_json("./data/bova11.json", orient="index")
        bova11.index = pd.to_datetime(bova11.index)

        #Criar o gráfico com as 3 séries juntas
        fig = go.Figure()

        #Criar o gráfico da estratégia
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=data.values, 
            mode='lines', 
            name='Estratégia', 
            line=dict(width=2, color='rgba(30, 184, 102, 1)')  # Linha verde
        ))

        #Criar o gráfico do CDI
        fig.add_trace(go.Scatter(
            x=cdi.index, 
            y=cdi[0].values, 
            mode='lines', 
            name='CDI', 
            line=dict(width=2, color='rgba(255, 0, 0, 1)')  # Linha vermelha
        ))

        #Criar o gráfico do IPCA
        fig.add_trace(go.Scatter(
            x=ipca.index, 
            y=ipca[0].values, 
            mode='lines', 
            name='IPCA', 
            line=dict(width=2, color='rgba(0, 0, 255, 1)')  # Linha azul
        ))

        #Criar o gráfico do BOVA11
        fig.add_trace(go.Scatter(
            x=bova11.index,
            y=bova11[0].values,
            mode='lines',
            name='BOVA11',            
            line=dict(width=2, color='rgba(255, 165, 0, 1)')
        ))
        
        fig.update_layout(
            font=dict(
                size=12,
            ),
            plot_bgcolor='white',  # Fundo branco
            paper_bgcolor='white',  # Fundo branco
            xaxis=dict(showgrid=False, title=''),  # Remover grades do eixo x e título
            yaxis=dict(showgrid=False, title='(%)'),  # Remover grades do eixo y e título
            showlegend=True,  # Remover a legenda
            # title='Desempenho da estratégia',  # Remover o título
            width=1200,  # Largura do gráfico em pixels (7.57 polegadas)
            height=350,  # Altura do gráfico em pixels (2.32 polegadas)
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return fig, data.iloc[-1], cdi.iloc[-1].values[0], ipca.iloc[-1].values[0], bova11.iloc[-1].values[0]

    def create_curve_capital_and_monthly_returns(self):
        
        data = self.track_record_strategy()

        df = pd.DataFrame(data[0])

        tr_portfolios = df['result']

        # Criar o gráfico
        fig1 = go.Figure()

        # Criar gráfico de uma série histórica com o datetime e o result
        fig1.add_trace(go.Scatter(
            x=tr_portfolios.index, 
            y=tr_portfolios.values, 
            mode='lines', 
            name='Result', 
            line=dict(width=2, color='rgba(30, 184, 102, 1)')  # Linha verde
        ))

        # Adicionar uma área sombreada com alta opacidade
        fig1.add_trace(go.Scatter(
            x=tr_portfolios.index,
            y=tr_portfolios.values,
            fill='tozeroy',
            mode='none',
            fillcolor='rgba(30, 184, 102, 0.15)',  # Cor verde com opacidade de 80%
            showlegend=False
        ))

        fig1.update_layout(
            font=dict(
                size=12,
            ),
            plot_bgcolor='white',  # Fundo branco
            paper_bgcolor='white',  # Fundo branco
            xaxis=dict(showgrid=False, title='', tickformat='%b %Y'),  # Remover grades do eixo x e título
            yaxis=dict(showgrid=False, title='', range=[min(tr_portfolios.values) - 1000, max(tr_portfolios.values)]),  # Remover grades do eixo y e título, ajustar o intervalo do eixo y
            showlegend=False,  # Remover a legenda
            # title='Curva de capital',  # Remover o título
            width=1200,  # Largura do gráfico em pixels (7.57 polegadas)
            height=350,  # Altura do gráfico em pixels (2.32 polegadas)            

        )

        #Monthly returns
        monthly_returns_df = self.monthly_returns(tr_portfolios)

        # Inverter a ordem dos anos
        monthly_returns_df = monthly_returns_df.iloc[::-1]

        # Gerar um heatmap com cores personalizadas e valores exibidos
        trace = go.Heatmap(
            z=monthly_returns_df.values.tolist(),
            x=monthly_returns_df.columns,
            y=monthly_returns_df.index,
            colorscale=[
                    [0, '#DD5B5B'],  # Vermelho para valores baixos (negativos)
                    [0.5, '#FFFFFF'],  # Branco para valores próximos de zero
                    [1, '#1EB866']  # Verde para valores altos (positivos)
                ],
            zmin=-10,  # Valor mínimo para a escala de cores
            zmax=10,  # Valor máximo para a escala de cores
            colorbar=dict(title='Retornos'),  # Legenda para o heatmap
            text= monthly_returns_df.values.tolist(), 
            texttemplate="%{text:.2f}",  # Formatar a exibição dos valores para duas casas decimais
            showscale=True  # Mostrar a escala de cores
        )
        
        layout = go.Layout(
            # title='Retornos mensais',
            xaxis=dict(title='Meses (%)'),
            yaxis=dict(title='Anos'),
            plot_bgcolor='white',  # Fundo branco
            paper_bgcolor='white',  # Fundo branco
            width=1200,  # Largura do gráfico em pixels para A4
            height=350,  # Altura do gráfico em pixels para A4
            # margin=dict(l=20, r=20, t=20, b=20)  # Ajustar margens conforme necessário
        )
        
        fig2 = go.Figure(data=[trace], layout=layout)

        return fig1, fig2,

    def create_strategy_statistics(self):

        stat = self.track_record_strategy()
        return stat

    def generate_benchmark(self):

        print("Gerando benchmark...")

        #Pegar os dados do CDI para o mesmo período
        #Dados do CDI
        cdi_serie = 12
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json&dataInicial={}&dataFinal={}".format(cdi_serie, self.data_inicial, self.data_final)
        cdi = pd.read_json(url)
        cdi['data'] = pd.to_datetime(cdi['data'], format='%d/%m/%Y')
        cdi.set_index('data', inplace=True)        
        cdi = cdi['valor'].astype(float).cumsum()
        cdi.fillna(0, inplace=True)
        cdi.to_json("./data/cdi.json", orient="index")

        #Dados do BOVA11 através do yahoo finance
        bova11 = yf.download('BOVA11.SA', start=datetime.datetime.strptime(self.data_inicial, "%d/%m/%Y"), end=datetime.datetime.strptime(self.data_final, "%d/%m/%Y"))
        bova11 = ((bova11['Adj Close'].pct_change() + 1).cumprod() - 1) * 100
        bova11.fillna(0, inplace=True)

        #Escrever em uma arquivo json.
        bova11.to_json("./data/bova11.json", orient="index")
                    
        time.sleep(20)

        #Dados do IPCA
        ipca_serie = 433
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json&dataInicial={}&dataFinal={}".format(ipca_serie, self.data_inicial, self.data_final)
        ipca = pd.read_json(url)
        ipca['data'] = pd.to_datetime(ipca['data'], format='%d/%m/%Y')
        ipca.set_index('data', inplace=True)
        ipca = ipca['valor'].astype(float).cumsum()
        ipca.fillna(0, inplace=True)

        #Escrever em uma arquivo json.
        ipca.to_json("./data/ipca.json", orient="index")

    def get_initial_end_date(self):
        return self.data_inicial, self.data_final

    def get_partner_links(self):
        pass
        
if __name__ == "__main__":
    strategy = StrategyDetails(155)
    # strategy.create_strategy_statistics()
    strategy.track_record_strategy()
    strategy.generate_benchmark()

    # strategy_data = strategy.create_curve_capital_and_monthly_returns()

    # portfolio.track_record_portfolio_2()
    # portfolio.create_strategy_performance()
