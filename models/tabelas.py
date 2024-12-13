"""Modulo para definir as tabelas do banco de dados. models/tabelas.py"""

import os
from urllib.parse import quote

from dotenv import load_dotenv
from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    create_engine,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

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


@relationship
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

    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome}, sobrenome={self.sobrenome})"

    def __str__(self):
        return self.nome


@relationship
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
    # Definindo a relação com a tabela orçamentos
    orcamentos = relationship("Orcamento", back_populates="cliente")
    # Adicionando o relacionamento na tabela Cliente
    projetos = relationship("Projeto", back_populates="cliente")

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf})"

    def __str__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf})"


@relationship
class Projeto(Base):
    """Classe para representar a tabela de projetos."""

    __tablename__ = "projetos"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    custo_estimado = Column(Numeric(precision=10, scale=2), nullable=True)
    cliente_id = Column(BigInteger, ForeignKey("clientes.id"), nullable=False)
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)  # pylint: disable=E1102
    atualizado_em = Column(
        TIMESTAMP,
        server_default=func.now(),  # pylint: disable=E1102
        onupdate=func.now(),  # pylint: disable=E1102
        nullable=True,
    )

    # Relacionamento com a tabela Cliente
    cliente = relationship("Cliente", back_populates="projetos")


class Orcamento(Base):
    """Classe para representar a tabela de orçamentos."""

    __tablename__ = "orcamentos"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cliente_id = Column(BigInteger, ForeignKey("clientes.id"), nullable=False)
    descricao = Column(String, nullable=True)
    data_criacao = Column(DateTime, default=func.now, nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=True)

    cliente = relationship("Cliente", back_populates="orcamentos")
    fundacoes = relationship("Fundacao", back_populates="orcamento")
    contrapisos = relationship("Contrapiso", back_populates="orcamento")
    lajes = relationship("Laje", back_populates="orcamento")
    telhados = relationship("Telhado", back_populates="orcamento")
    eletricas = relationship("Eletrica", back_populates="orcamento")
    paredes = relationship("Parede", back_populates="orcamento")

    def __repr__(self):
        return f"Orcamento(id={self.id}, cliente_id={self.cliente_id}, descricao={self.descricao})"

    def __str__(self):
        return f"Orcamento(id={self.id}, cliente_id={self.cliente_id}, descricao={self.descricao})"


# Classes para tabelas específicas
class Fundacao(Base):
    """Classe para representar a tabela de fundacoes."""

    __tablename__ = "fundacoes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    orcamento_id = Column(
        BigInteger, ForeignKey("orcamentos.id", ondelete="CASCADE"), nullable=False
    )
    comprimento = Column(Numeric(10, 2), nullable=False)
    largura = Column(Numeric(10, 2), nullable=False)
    espessura = Column(Numeric(10, 2), nullable=False)
    valor_m3 = Column(Numeric(10, 2), nullable=False)
    custo_total = Column(Numeric(10, 2), nullable=False)

    orcamento = relationship("Orcamento", back_populates="fundacoes")


class Contrapiso(Base):
    """Classe para representar a tabela de contrapisos."""

    __tablename__ = "contrapisos"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    orcamento_id = Column(
        BigInteger, ForeignKey("orcamentos.id", ondelete="CASCADE"), nullable=False
    )
    comprimento = Column(Numeric(10, 2), nullable=False)
    largura = Column(Numeric(10, 2), nullable=False)
    espessura = Column(Numeric(10, 2), nullable=True)
    valor_metro = Column(Numeric(10, 2), nullable=False)
    custo_total = Column(Numeric(10, 2), nullable=False)

    orcamento = relationship("Orcamento", back_populates="contrapisos")


class Laje(Base):
    """Classe para representar a tabela de lajes."""

    __tablename__ = "lajes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    orcamento_id = Column(
        BigInteger, ForeignKey("orcamentos.id", ondelete="CASCADE"), nullable=False
    )
    comprimento = Column(Numeric(10, 2), nullable=False)
    largura = Column(Numeric(10, 2), nullable=False)
    espessura = Column(Numeric(10, 2), nullable=False)
    valor_m3 = Column(Numeric(10, 2), nullable=False)
    custo_total = Column(Numeric(10, 2), nullable=False)

    orcamento = relationship("Orcamento", back_populates="lajes")


class Telhado(Base):
    """Classe para representar a tabela de telhados."""

    __tablename__ = "telhados"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    orcamento_id = Column(
        BigInteger, ForeignKey("orcamentos.id", ondelete="CASCADE"), nullable=False
    )
    comprimento = Column(Numeric(10, 2), nullable=False)
    largura = Column(Numeric(10, 2), nullable=False)
    valor_metro = Column(Numeric(10, 2), nullable=False)
    custo_total = Column(Numeric(10, 2), nullable=False)

    orcamento = relationship("Orcamento", back_populates="telhados")


class Eletrica(Base):
    """Classe para representar a tabela de eletricas."""

    __tablename__ = "eletricas"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    orcamento_id = Column(
        BigInteger, ForeignKey("orcamentos.id", ondelete="CASCADE"), nullable=False
    )
    pontos_eletricos = Column(BigInteger, nullable=False)
    valor_por_ponto = Column(Numeric(10, 2), nullable=False)
    custo_total = Column(Numeric(10, 2), nullable=False)

    orcamento = relationship("Orcamento", back_populates="eletricas")


class Parede(Base):
    """Classe para representar a tabela de paredes."""

    __tablename__ = "paredes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    orcamento_id = Column(
        BigInteger, ForeignKey("orcamentos.id", ondelete="CASCADE"), nullable=False
    )
    altura = Column(Numeric(10, 2), nullable=False)
    comprimento = Column(Numeric(10, 2), nullable=False)
    valor_m2 = Column(Numeric(10, 2), nullable=False)
    custo_total = Column(Numeric(10, 2), nullable=False)

    orcamento = relationship("Orcamento", back_populates="paredes")


@relationship
class Modulos(Base):
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

    def __repr__(self):
        return f"<Modulo(id={self.id}, user_id={self.user_id}, parede={self.parede}, contrapiso={self.contrapiso}, eletrica={self.eletrica}, fundacao={self.fundacao}, laje={self.laje}, telhado={self.telhado})>"  # pylint: disable=line-too-long

    def __str__(self):
        return f"Modulo(id={self.id}, user_id={self.user_id}, parede={self.parede}, contrapiso={self.contrapiso}, eletrica={self.eletrica}, fundacao={self.fundacao}, laje={self.laje}, telhado={self.telhado})"  # pylint: disable=line-too-long


@relationship
class Feedback(Base):
    """Classe para representar a tabela de feedbacks."""

    __tablename__ = "feedbacks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cliente_nome = Column(String, nullable=False)
    feedback = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Feedback(cliente_nome={self.cliente_nome}, feedback={self.feedback})>"

    def __str__(self):
        return f"Feedback de {self.cliente_nome}: {self.feedback}"


# Função para criar o banco de dados e as tabelas
def criar_tabelas():
    """Função para criar o banco de dados e as tabelas."""
    engine = create_engine(DATABASE_URL, echo=True)
    # Base.metadata.tables["usuarios"].create(bind=engine, checkfirst=True)
    # Base.metadata.tables["clientes"].create(bind=engine, checkfirst=True)
    # Base.metadata.tables["modulos"].create(bind=engine, checkfirst=True)
    # Base.metadata.tables["orcamentos"].create(bind=engine, checkfirst=True)
    # Base.metadata.tables["projetos"].create(bind=engine, checkfirst=True)
    # Base.metadata.tables["feedbacks"].create(bind=engine, checkfirst=True)
    Base.metadata.create_all(engine)  # pylint: disable=no-member
    print("Tabelas criadas com sucesso!")


if __name__ == "__main__":
    criar_tabelas()
