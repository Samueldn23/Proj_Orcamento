"""configurações do banco de dados. db_config.py"""

import os
from urllib.parse import quote

import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

db_pass_cod = quote(db_pass)


def get_connection(event=None):  # pylint: disable=unused-argument
    """Retorna uma conexão com o banco de dados"""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres.whccjbodlnfmublrssmq",
            password=db_pass_cod,
            host="aws-0-sa-east-1.pooler.supabase.com",  # ou o IP do servidor
            port=6543,
        )
        print("Conexão bem-sucedida!")

        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        raise
