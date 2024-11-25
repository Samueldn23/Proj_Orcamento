"""Base de dados db.py"""

import os
from urllib.parse import quote

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

Base = declarative_base()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
nome = os.getenv("DB_NAME")
password_codificada = quote(password)


DATABASE_URL = f"postgresql://{user}:{password_codificada}@{host}/{nome}"
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)


def criar_tabelas():
    """Cria as tabelas no banco de dados."""
    Base.metadata.create_all(bind=engine)
