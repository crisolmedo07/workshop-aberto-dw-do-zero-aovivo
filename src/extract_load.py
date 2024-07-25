# import
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


# import das variables de ambiente
load_dotenv()

commodities = ['CL=F' , 'GC=F' , 'SI=F'] # activos de bolsa de valores

# busca las variables de ambientes con la biblioteca dotenv
DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD') 
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')
    
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

# pegar a cotação dos activos

def buscar_dados_de_commodities( simbolo , periodo = '5y' , intervalo = '1d' ):
    ticker = yf.Ticker(simbolo)
    dados = ticker.history(period = periodo , interval = intervalo )[['Close']]
    dados['simbolo'] = simbolo
    return dados

# concatenar os meus ativos (1..2..3) -> (1)
def buscar_todos_dados_commodities(commodities):
    todos_dados = []
    for simbolo in commodities:
        dados = buscar_dados_de_commodities(simbolo)
        todos_dados.append(dados)
    return pd.concat(todos_dados)

# salvar no banco de datos
def salvar_no_postgres( df , schema = 'public'):
    df.to_sql('commodities' , engine , if_exists = 'replace' , index = True , index_label = 'Date' , schema = schema ) #if_exists = append (agregar datos)
if __name__ == "__main__":
    dados_concatenados = buscar_todos_dados_commodities(commodities)
    salvar_no_postgres(dados_concatenados , schema='public')











