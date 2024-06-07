from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_apscheduler import APScheduler
import pyodbc
import requests
import logging
from colorama import Fore, Style  # Importando a biblioteca colorama
import art  # Importando a biblioteca art
import time
from threading import Lock

app = Flask(__name__)

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DataInsertLogger")
# Agora você pode usar o colorama para colorir seus logs
logger.info(Fore.GREEN + "Iniciando o aplicativo..." + Style.RESET_ALL)
# Exibindo a arte ASCII com o nome "CPM"
print(art.text2art("CPM COMMBOX "))

lock = Lock()  # Lock para controlar a execução única

def create_conn():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=DESKTOP-N8FU06Q;'
                          'DATABASE=commbox_sca;'
                          'Trusted_Connection=yes;')
    return conn

def format_cpf(cpf):
    """Formata o CPF no formato 000.099.555-00."""
    cpf = cpf.zfill(11)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def check_duplicate_cpf(cursor, cpf):
    """Verifica se o CPF já existe no banco de dados."""
    cursor.execute("SELECT COUNT(*) FROM CBX_USUARIO WHERE CPF_CNPJ = ?", cpf)
    return cursor.fetchone()[0] > 0

def insert_data_to_table(data):
    conn = create_conn()
    cursor = conn.cursor()
    try:
        for contractor in data:
            # Validando se todos os campos necessários estão presentes
            if ("National ID" in contractor and "Worker ID" in contractor and
                "First Name" in contractor and "Last Name" in contractor and
                "Worker Email" in contractor and "Site Name" in contractor and
                "Cost Center Code" in contractor):
                
                formatted_cpf = format_cpf(contractor["National ID"])

                try:
                    # Iniciar transação
                    cursor.execute("BEGIN TRANSACTION")

                    # Verificar se o CPF já existe no banco de dados
                    if check_duplicate_cpf(cursor, formatted_cpf):
                        logger.info(f"CPF {formatted_cpf} já existe no banco de dados. Ignorando inserção.")
                        cursor.execute("ROLLBACK")
                        continue

                    # Buscar o maior valor de ID_USUARIO
                    cursor.execute("SELECT MAX(ID_USUARIO) FROM CBX_USUARIO")
                    last_id = cursor.fetchone()[0]
                    next_id = last_id + 1 if last_id is not None else 1

                    cursor.execute("""
                        INSERT INTO CBX_USUARIO (ID_USUARIO, CPF_CNPJ, PANCARY, NOME, EMAIL, NOME_DOMINIO_ORIGEM, PAI, ID_DOMINIO)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        next_id,
                        formatted_cpf,
                        contractor["Worker ID"],
                        f"{contractor['First Name']} {contractor['Last Name']}",
                        contractor["Worker Email"],
                        contractor["Site Name"],
                        contractor["Cost Center Code"],
                        1  # Valor fixo para ID_DOMINIO
                    ))
                    # Confirmar transação
                    cursor.execute("COMMIT")
                    logger.info(f"CPF {formatted_cpf} inserido com sucesso no banco de dados.")
                
                except Exception as e:
                    cursor.execute("ROLLBACK")
                    logger.error(f"Erro ao inserir dados: {e}")

        conn.commit()
        logger.info("Successfully inserted records into the database.")
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
    finally:
        conn.close()


def fetch_and_insert_data():
    if not lock.acquire(blocking=False):
        logger.info("fetch_and_insert_data job is already running. Skipping this execution.")
        return    
    try:
        start_time = time.time()
        logger.info("Starting fetch_and_insert_data job...")

        # URL da API e parâmetros de autenticação
        api_url = "https://gaip-api-qa.ap.angloamerican.com/pxapi/datasphere/contractor-access-control-br/get-contractors"
        token_url = "https://aaop.int1.eu.fieldglasstest.cloud.sap/api/oauth2/v2.0/token"
        client_id = "Integration_NONSAP_commbox"
        client_secret = "AAOP_THTGlpdT5Y353shYhMBBTphq92f"
        subscription_key = "94323f0ade9c46fc913d716302bd6c5a"

        # Obter token de acesso
        auth_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
        headers = {
            "Ocp-Apim-Subscription-Key": subscription_key
        }
        try:
            response = requests.post(token_url, data=auth_data, headers=headers)
            if response.status_code == 200:
                access_token = response.json()["access_token"]
                # Fazer solicitação GET com o token de acesso
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Ocp-Apim-Subscription-Key": subscription_key
                }
                response = requests.get(api_url, headers=headers)
                if response.status_code == 200:
                    try:
                        data = response.json().get("data", [])
                        insert_data_to_table(data)
                    except ValueError as e:
                        logger.error(f"JSON decoding error: {e}")
                else:
                    logger.error(f"Failed to fetch data: {response.status_code}")
            else:
                logger.error(f"Failed to obtain access token: {response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
        finally:
            end_time = time.time()
            logger.info(f"fetch_and_insert_data job completed in {end_time - start_time} seconds")
    finally:
        lock.release()


if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='fetch_and_insert_data', func=fetch_and_insert_data, trigger='interval', minutes=1)
    fetch_and_insert_data()  # Inserir dados no banco de dados ao iniciar o aplicativo
    app.run(debug=True)
