from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Tabela para a edificação/instalação
class Edificacao(Base):
    __tablename__ = 'edificacao'

    id = Column(Integer, primary_key=True)
    razao_social = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    telefone = Column(String)
    email = Column(String)
    altura_total = Column(Integer)
    perimetro = Column(Integer)

    # Relacionamento com as inspeções
    inspecoes = relationship("Inspecao", back_populates="edificacao")

# Tabela para as inspeções de SPDA
class Inspecao(Base):
    __tablename__ = 'inspecao'

    id = Column(Integer, primary_key=True)
    data_inspecao = Column(DateTime, default=datetime.utcnow)
    tecnico = Column(String, nullable=False)
    observacoes = Column(String)
    edificacao_id = Column(Integer, ForeignKey('edificacao.id'))

    # Relacionamento com a edificação e os itens da inspeção
    edificacao = relationship("Edificacao", back_populates="inspecoes")
    itens = relationship("ItemInspecao", back_populates="inspecao")

# Tabela para cada item de inspeção
class ItemInspecao(Base):
    __tablename__ = 'item_inspecao'

    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    conforme = Column(Boolean, nullable=False)
    inspecao_id = Column(Integer, ForeignKey('inspecao.id'))

    # Relacionamento com a inspeção
    inspecao = relationship("Inspecao", back_populates="itens")
