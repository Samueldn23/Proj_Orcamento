"""Modulo para definir as tabelas do banco de dados. models/tabelas.py"""

import os
from urllib.parse import quote

from dotenv import load_dotenv
from sqlalchemy import (
    TIMESTAMP,
    Column,
    Date,
    ForeignKey,
    BigInteger,
    String,
    Numeric,
    Boolean,
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

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
    )

    nome = Column(String(255), nullable=False)
    sobrenome = Column(String(255), nullable=True)
    telefone = Column(String(15), nullable=True)
    endereco = Column(String, nullable=True)
    data_nascimento = Column(Date, nullable=True)
    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),  # pylint: disable=E1102
        nullable=True,
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),  # pylint: disable=E1102
        onupdate=func.now(),  # pylint: disable=E1102
        nullable=True,
    )

    # Relacionamento de 1 para muitos com clientes
    clientes = relationship("Cliente", back_populates="usuario")
    modulos = relationship("Modulo", back_populates="usuario")


# Classe para a tabela Cliente
class Cliente(Base):
    """Classe para representar a tabela de clientes."""

    __tablename__ = "clientes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.user_id"), nullable=False
    )  # Chave estrangeira
    nome = Column(String, nullable=True)
    cpf = Column(Numeric, nullable=True)
    telefone = Column(Numeric, nullable=False, unique=True)
    email = Column(String, nullable=True)
    endereco = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    cep = Column(Numeric, nullable=True)
    bairro = Column(String, nullable=True)
    numero = Column(String, nullable=True)

    # Definindo a relação com a tabela usuarios
    usuario = relationship("Usuario", back_populates="clientes")


class Modulo(Base):
    """Classe para representar a tabela de módulos."""

    __tablename__ = "modulos"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    parede = Column(Boolean, nullable=False, default=True)
    contrapiso = Column(Boolean, nullable=False, default=False)
    eletrica = Column(Boolean, nullable=False, default=False)
    fundacao = Column(Boolean, nullable=False, default=False)
    laje = Column(Boolean, nullable=False, default=False)
    telhado = Column(Boolean, nullable=False, default=False)

    # Relacionamento de um para um com Usuario
    usuario = relationship("Usuario", back_populates="modulos")


# Função para criar o banco de dados e as tabelas
def criar_tabelas():
    """Função para criar o banco de dados e as tabelas."""
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.tables["usuarios"].create(bind=engine, checkfirst=True)
    Base.metadata.tables["clientes"].create(bind=engine, checkfirst=True)
    Base.metadata.tables["modulos"].create(bind=engine, checkfirst=True)
    print("Tabelas criadas com sucesso!")


if __name__ == "__main__":
    criar_tabelas()
