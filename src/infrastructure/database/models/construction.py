"""Models de construção"""

from sqlalchemy import Column, BigInteger, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Foundation(Base):
    """Modelo de fundação no banco de dados"""

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

    orcamento = relationship("Budget", back_populates="fundacoes")


class Floor(Base):
    """Modelo de contrapiso no banco de dados"""

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

    orcamento = relationship("Budget", back_populates="contrapisos")


class Slab(Base):
    """Modelo de laje no banco de dados"""

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

    orcamento = relationship("Budget", back_populates="lajes")


class Roof(Base):
    """Modelo de telhado no banco de dados"""

    __tablename__ = "telhados"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    orcamento_id = Column(
        BigInteger, ForeignKey("orcamentos.id", ondelete="CASCADE"), nullable=False
    )
    comprimento = Column(Numeric(10, 2), nullable=False)
    largura = Column(Numeric(10, 2), nullable=False)
    valor_metro = Column(Numeric(10, 2), nullable=False)
    custo_total = Column(Numeric(10, 2), nullable=False)

    orcamento = relationship("Budget", back_populates="telhados")


class Electrical(Base):
    """Modelo de elétrica no banco de dados"""

    __tablename__ = "eletricas"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    orcamento_id = Column(
        BigInteger, ForeignKey("orcamentos.id", ondelete="CASCADE"), nullable=False
    )
    pontos_eletricos = Column(BigInteger, nullable=False)
    valor_por_ponto = Column(Numeric(10, 2), nullable=False)
    custo_total = Column(Numeric(10, 2), nullable=False)

    orcamento = relationship("Budget", back_populates="eletricas")


class Wall(Base):
    """Modelo de parede no banco de dados"""

    __tablename__ = "paredes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    orcamento_id = Column(
        BigInteger, ForeignKey("orcamentos.id", ondelete="CASCADE"), nullable=False
    )
    altura = Column(Numeric(10, 2), nullable=False)
    comprimento = Column(Numeric(10, 2), nullable=False)
    valor_m2 = Column(Numeric(10, 2), nullable=False)
    custo_total = Column(Numeric(10, 2), nullable=False)

    orcamento = relationship("Budget", back_populates="paredes")
