"""Model de cliente"""

from sqlalchemy import Column, BigInteger, String, ForeignKey, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base


class Client(Base):
    """Modelo de cliente no banco de dados"""

    __tablename__ = "clientes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.user_id"), nullable=False)
    nome = Column(String(255), nullable=False)
    cpf = Column(String, nullable=True)
    telefone = Column(String(20))
    email = Column(String(255))
    endereco = Column(Text)
    cidade = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    cep = Column(String, nullable=True)
    bairro = Column(String, nullable=True)
    numero = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relacionamentos - remover referência a orçamentos
    usuario = relationship("User", back_populates="clientes")
    projetos = relationship(
        "Project", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome})"
