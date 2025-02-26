"""Model de orçamento"""

from sqlalchemy import Column, BigInteger, String, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .base import Base


class Budget(Base):
    """Modelo de orçamento no banco de dados"""

    __tablename__ = "orcamentos"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cliente_id = Column(BigInteger, ForeignKey("clientes.id"), nullable=False)
    descricao = Column(String, nullable=True)
    data_criacao = Column(DateTime, default=func.now(), nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=True)

    # Relacionamentos
    cliente = relationship("Client", back_populates="orcamentos")
    fundacoes = relationship("Foundation", back_populates="orcamento")
    contrapisos = relationship("Floor", back_populates="orcamento")
    lajes = relationship("Slab", back_populates="orcamento")
    telhados = relationship("Roof", back_populates="orcamento")
    eletricas = relationship("Electrical", back_populates="orcamento")
    paredes = relationship("Wall", back_populates="orcamento")
    projetos = relationship("Project", back_populates="budget")

    def __repr__(self):
        return f"Orcamento(id={self.id}, cliente_id={self.cliente_id})"
