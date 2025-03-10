"""Model de módulos"""

from typing import ClassVar

from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Module(Base):
    """Modelo de módulos no banco de dados"""

    __tablename__ = "modulos"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.user_id"), nullable=False)
    user_name = Column(String, nullable=False)
    parede = Column(Boolean, default=True)
    contrapiso = Column(Boolean, default=False)
    eletrica = Column(Boolean, default=False)
    fundacao = Column(Boolean, default=False)
    laje = Column(Boolean, default=False)
    telhado = Column(Boolean, default=False)

    # Definir explicitamente as propriedades a serem mapeadas
    __mapper_args__: ClassVar[dict[str, list[str]]] = {
        "include_properties": ["id", "user_id", "user_name", "parede", "contrapiso", "eletrica", "fundacao", "laje", "telhado"]
    }

    # Relacionamentos
    usuario = relationship("User", back_populates="modulos")

    def __repr__(self):
        return f"Module(id={self.id}, user_id={self.user_id})"
