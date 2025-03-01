"""Model de fundação"""

from sqlalchemy import BigInteger, Column, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import relationship

from .base import Base


class Foundation(Base):
    """Modelo de fundação no banco de dados"""

    __tablename__ = "fundacoes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    projeto_id = Column(BigInteger, ForeignKey("projetos.id"), nullable=False)
    tipo = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    dimensoes = Column(String(100), nullable=True)
    quantidade = Column(Numeric(10, 2), nullable=False)
    valor_unitario = Column(Numeric(10, 2), nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=False)

    # Relacionamentos
    projeto = relationship("Project", back_populates="fundacoes")

    def __repr__(self):
        return f"Foundation(id={self.id}, projeto_id={self.projeto_id})"
