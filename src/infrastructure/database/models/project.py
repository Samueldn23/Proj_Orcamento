"""Model de projeto"""

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    Numeric,
    ForeignKey,
    TIMESTAMP,
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
    atualizado_em = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True
    )

    # Relacionamentos
    cliente = relationship("Client", back_populates="projetos")

    def __repr__(self):
        return f"Project(id={self.id}, nome={self.nome})"
