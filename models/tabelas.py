"""Tabelas do banco de dados tabelas.py"""

from sqlalchemy import Column, Integer, String

from models.db_sql import Base


class Cliente(Base):
    """tabela de clientes"""

    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    endereco = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    cep = Column(String, nullable=True)
    bairro = Column(String, nullable=True)
    numero = Column(String, nullable=True)

    # Sobrescrevendo o __repr__ para exibir as informações de forma legível
    def __repr__(self):
        return f"<Cliente(id:{self.id}, nome:{self.nome}, cpf:{self.cpf}, telefone:{self.telefone}, email:{self.email})>"  # pylint: disable=line-too-long
