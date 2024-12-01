"""Modulo para definir as tabelas do banco de dados. tabelas.py"""

import os
from urllib.parse import quote

from dotenv import load_dotenv
from sqlalchemy import (
    TIMESTAMP,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    create_engine,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base


# Carregar variáveis de ambiente do arquivo .env
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

# Definição da base
Base = declarative_base()


# Classe para a tabela Usuario
class Usuario(Base):
    """Classe para representar a tabela de usuários."""

    __tablename__ = "usuarios"  # Nome no plural para consistência

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
    )  # ID único do usuário
    nome = Column(String(255), nullable=False)
    sobrenome = Column(String(255))
    telefone = Column(String(15))
    endereco = Column(String)
    data_nascimento = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.now())  # pylint: disable=E1102
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # pylint: disable=E1102

    # Relacionamento de 1 para muitos com clientes
    clientes = relationship("Cliente", back_populates="usuario")


# Classe para a tabela Cliente
class Cliente(Base):
    """Classe para representar a tabela de clientes."""

    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    nome = Column(String, nullable=True)
    cpf = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    endereco = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    cep = Column(String, nullable=True)
    bairro = Column(String, nullable=True)
    numero = Column(String, nullable=True)

    # Relacionamento de muitos para 1 com usuário
    usuario = relationship("Usuario", back_populates="clientes")


# Função para criar o banco de dados e as tabelas
def criar_tabelas():
    """Função para criar o banco de dados e as tabelas."""
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")


if __name__ == "__main__":
    criar_tabelas()
