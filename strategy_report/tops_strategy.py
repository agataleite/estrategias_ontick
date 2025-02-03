from sshtunnel import SSHTunnelForwarder, BaseSSHTunnelForwarderError
import pymysql
from dotenv import load_dotenv
import os
import pandas as pd

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

class StrategiesOnTick:
    
    def get_strategies_results(self):
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
                    
                    sql = """
                            SELECT ti.investment_name,
                                ts.strategy_developer, 
                                SUM(tp.position_profit) as total_pnl,
                                MAX(tp.position_volume_open_max) as max_volume_strategy,
                                COUNT(*) as total_operacoes
                            FROM tb_positions tp
                            INNER JOIN tb_investments ti ON tp.investment_id = ti.investment_id
                            INNER JOIN tb_strategies ts ON ts.strategy_id = ti.strategy_id
                            WHERE tp.investment_id IN (
                                SELECT B.investment_id
                                FROM tb_strategies A
                                INNER JOIN tb_track_record B ON A.track_record_id = B.tr_id
                                WHERE A.strategy_status = 'ACTIVE'
                                AND B.tr_num_trades > 0
                                AND B.tr_history_splits IS NOT NULL
                                ORDER BY A.strategy_developer ASC, B.investment_id ASC
                            )
                            AND position_time_open >= '2024-09-01'
                            AND position_time_open <= '2024-10-01'
                            GROUP BY ti.investment_name, ts.strategy_developer
                            ORDER BY ts.strategy_developer ASC, ti.investment_name ASC;
                        """                    
                    cursor.execute(sql)
                    result = cursor.fetchall()

                    #Salvar em DataFrame
                    df = pd.DataFrame(result, columns=["investment_name", "strategy_developer", "pnl", "max_volume_strategy", "total_operacoes"])
                    #Passar a coluna pnl para float
                    df["pnl"] = df["pnl"].astype(float)
                    df["max_volume_strategy"] = df["max_volume_strategy"].astype(int)
                    df = df.sort_values("pnl", ascending=False)
                    df.reset_index(drop=True, inplace=True)                    
                    print(df)

                    #Salvar em um excel
                    df.to_excel("strategies_results.xlsx", index=False)
                    print(df.head(50))
                    print("Arquivo EXCEL salvo com sucesso!")


            except BaseSSHTunnelForwarderError as e:
                print(f"Erro ao criar o túnel SSH: {e}")
            except pymysql.MySQLError as e:
                print(f"Erro ao conectar ao banco de dados: {e}")
            finally:
                # Fechando a conexão
                connection.close()

    def read_csv(self):

        df = pd.read_csv("strategies_results.csv")

        #Somar todos os resultados de cada investment_id
        df = df.groupby("investment_name").sum()
        df.reset_index(inplace=True)

        #Ordenar por pnl
        df = df.sort_values("pnl", ascending=False)
        df.reset_index(drop=True, inplace=True)

        #Salvar em um excel
        df.to_excel("strategies_results.xlsx", index=False)
        print(df.head(50))


if __name__ == "__main__":
    strategy = StrategiesOnTick()
    strategy.get_strategies_results()
    # strategy.read_csv()


