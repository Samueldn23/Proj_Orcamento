"""Model de cliente"""

from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base


class Client(Base):
    """Modelo de cliente no banco de dados"""

    __tablename__ = "clientes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.user_id"), nullable=False)
    nome = Column(String, nullable=True)
    cpf = Column(String, nullable=True)
    telefone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    endereco = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    cep = Column(String, nullable=True)
    bairro = Column(String, nullable=True)
    numero = Column(String, nullable=True)

    # Relacionamentos
    usuario = relationship("User", back_populates="clientes")
    orcamentos = relationship("Budget", back_populates="cliente")
    projetos = relationship("Project", back_populates="cliente")

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf})"
