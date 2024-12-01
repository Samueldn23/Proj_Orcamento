"""configurações do banco de dados. db_sql.py"""

import os
from urllib.parse import quote

import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()

# Configurações do banco de dados
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Codificando a senha para evitar problemas com caracteres especiais
DB_PASS_CODIFICADA = quote(DB_PASS)

# URL de conexão do SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS_CODIFICADA}@{DB_HOST}/{DB_NAME}"

# Criar o engine e a sessão do SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

Base.metadata.create_all(bind=engine)


def get_connection(event=None):  # pylint: disable=unused-argument
    """Retorna uma conexão com o banco de dados"""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres.whccjbodlnfmublrssmq",
            password=DB_PASS_CODIFICADA,
            host="aws-0-sa-east-1.pooler.supabase.com",  # ou o IP do servidor
            port=6543,
        )
        print("Conexão bem-sucedida!")

        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        raise


def obter_conexao_sqlalchemy():
    """Retorna uma nova sessão do SQLAlchemy."""
    return Session()


#
