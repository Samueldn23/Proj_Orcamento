"""Model de usuário"""

from sqlalchemy import TIMESTAMP, BigInteger, Column, Date, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    """Modelo de usuário no banco de dados"""

    __tablename__ = "usuarios"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    nome = Column(String(255), nullable=False)
    sobrenome = Column(String(255), nullable=True)
    telefone = Column(String(15), nullable=True)
    endereco = Column(String, nullable=True)
    data_nascimento = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True
    )

    # Relacionamentos
    clientes = relationship("Client", back_populates="usuario")
    modulos = relationship("Module", back_populates="usuario")

    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome})"
