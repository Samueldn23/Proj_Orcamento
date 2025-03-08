"""Models de construção"""

from sqlalchemy import BigInteger, Column, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from .base import Base


class Fundacoes(Base):
    """Modelo de fundação no banco de dados"""

    __tablename__ = "fundacoes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    projeto_id = Column(BigInteger, ForeignKey("projetos.id", ondelete="CASCADE"), nullable=False)
    comprimento = Column(Numeric(10, 2), nullable=False)
    largura = Column(Numeric(10, 2), nullable=False)
    espessura = Column(Numeric(10, 2), nullable=False)
    valor_m3 = Column(Numeric(10, 2), nullable=False)
    custo_total = Column(Numeric(10, 2), nullable=False)

    projeto = relationship("Projeto", back_populates="fundacoes")

    def __repr__(self):
        return f"Fundacao(id={self.id}, projeto_id={self.projeto_id})"


class Contrapisos(Base):
    """Modelo de contrapiso no banco de dados"""

    __tablename__ = "contrapisos"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    projeto_id = Column(BigInteger, ForeignKey("projetos.id", ondelete="CASCADE"), nullable=False)
    comprimento = Column(Numeric(10, 2), nullable=False)
    largura = Column(Numeric(10, 2), nullable=False)
    espessura = Column(Numeric(10, 2), nullable=True)
    valor_metro = Column(Numeric(10, 2), nullable=False)
    custo_total = Column(Numeric(10, 2), nullable=False)

    projeto = relationship("Projeto", back_populates="contrapisos")


class Lajes(Base):
    """Modelo de laje no banco de dados"""

    __tablename__ = "lajes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    projeto_id = Column(BigInteger, ForeignKey("projetos.id", ondelete="CASCADE"), nullable=False)
    comprimento = Column(Numeric(10, 2), nullable=False)
    largura = Column(Numeric(10, 2), nullable=False)
    espessura = Column(Numeric(10, 2), nullable=False)
    valor_m3 = Column(Numeric(10, 2), nullable=False)
    custo_total = Column(Numeric(10, 2), nullable=False)

    projeto = relationship("Projeto", back_populates="lajes")


class Telhados(Base):
    """Modelo de telhado no banco de dados"""

    __tablename__ = "telhados"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    projeto_id = Column(BigInteger, ForeignKey("projetos.id", ondelete="CASCADE"), nullable=False)
    comprimento = Column(Numeric(10, 2), nullable=False)
    largura = Column(Numeric(10, 2), nullable=False)
    valor_metro = Column(Numeric(10, 2), nullable=False)
    custo_total = Column(Numeric(10, 2), nullable=False)

    projeto = relationship("Projeto", back_populates="telhados")


class Eletricas(Base):
    """Modelo de elétrica no banco de dados"""

    __tablename__ = "eletricas"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    projeto_id = Column(BigInteger, ForeignKey("projetos.id", ondelete="CASCADE"), nullable=False)
    pontos_eletricos = Column(BigInteger, nullable=False)
    valor_por_ponto = Column(Numeric(10, 2), nullable=False)
    custo_total = Column(Numeric(10, 2), nullable=False)

    projeto = relationship("Projeto", back_populates="eletricas")


class Paredes(Base):
    """Modelo de parede no banco de dados"""

    __tablename__ = "paredes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    projeto_id = Column(BigInteger, ForeignKey("projetos.id", ondelete="CASCADE"), nullable=False)
    altura = Column(Numeric(10, 2), nullable=False)
    comprimento = Column(Numeric(10, 2), nullable=False)
    area = Column(Numeric(10, 2), nullable=False)
    valor_m2 = Column(Numeric(10, 2), nullable=False)
    tipo_tijolo = Column(String(100), nullable=False)
    quantidade_tijolos = Column(BigInteger, nullable=False)
    custo_tijolos = Column(Numeric(10, 2), nullable=False)
    custo_mao_obra = Column(Numeric(10, 2), nullable=False)
    custo_total = Column(Numeric(10, 2), nullable=False)

    projeto = relationship("Projeto", back_populates="paredes")
