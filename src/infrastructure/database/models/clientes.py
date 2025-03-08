"""Modelo de cliente"""

from typing import ClassVar

from sqlalchemy import BigInteger, Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Cliente(Base):
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

    # Tornando as colunas de data opcionais para compatibilidade
    # Se as colunas não existirem no banco, o SQLAlchemy não tentará acessá-las
    __mapper_args__: ClassVar[dict[str, list[str]]] = {
        "include_properties": ["id", "user_id", "nome", "cpf", "telefone", "email", "endereco", "cidade", "estado", "cep", "bairro", "numero"]
    }

    # Relacionamentos - remover referência a orçamentos
    usuario = relationship("Usuario", back_populates="clientes")
    projetos = relationship("Projeto", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome})"
