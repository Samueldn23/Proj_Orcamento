"""Model de projeto"""

from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    Column,
    ForeignKey,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from .base import Base


class Project(Base):
    """Modelo de projeto no banco de dados"""

    __tablename__ = "projetos"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    custo_estimado = Column(Numeric(precision=10, scale=2), nullable=True)
    cliente_id = Column(BigInteger, ForeignKey("clientes.id"), nullable=False)
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    atualizado_em = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True)
    valor_total = Column(Numeric(10, 2), nullable=True)

    # Relacionamentos - remover qualquer referência a orçamentos
    cliente = relationship("Client", back_populates="projetos")
    fundacoes = relationship("Foundation", back_populates="projeto", cascade="all, delete-orphan")
    contrapisos = relationship("Floor", back_populates="projeto", cascade="all, delete-orphan")
    lajes = relationship("Slab", back_populates="projeto", cascade="all, delete-orphan")
    telhados = relationship("Roof", back_populates="projeto", cascade="all, delete-orphan")
    eletricas = relationship("Electrical", back_populates="projeto", cascade="all, delete-orphan")
    paredes = relationship("Wall", back_populates="projeto", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Project(id={self.id}, nome={self.nome})"
