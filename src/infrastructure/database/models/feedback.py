"""Model de feedback"""

from sqlalchemy import Column, BigInteger, String, Text
from .base import Base


class Feedback(Base):
    """Modelo de feedback no banco de dados"""

    __tablename__ = "feedbacks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cliente_nome = Column(String, nullable=False)
    feedback = Column(Text, nullable=False)

    def __repr__(self):
        return f"Feedback(cliente_nome={self.cliente_nome})"
