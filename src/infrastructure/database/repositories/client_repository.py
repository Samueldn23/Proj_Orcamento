"""Repositório de clientes"""

from typing import Any

from src.infrastructure.cache.cache_config import cache_query

from ..connections.postgres import postgres
from ..models.clientes import Cliente


class ClientRepository:
    """Repositório para operações com clientes"""

    def __init__(self):
        self.db = postgres

    def create(
        self,
        user_id: str,
        nome: str,
        cpf: int,
        telefone: int,
        email: str,
        endereco: str,
        cidade: str,
        estado: str,
        cep: int,
        bairro: str,
        numero: str,
    ) -> Cliente | None:
        """Adiciona um novo cliente"""
        try:
            with self.db.get_session() as session:
                cliente = Cliente(
                    user_id=user_id,
                    nome=nome,
                    cpf=cpf,
                    telefone=telefone,
                    email=email,
                    endereco=endereco,
                    cidade=cidade,
                    estado=estado,
                    cep=cep,
                    bairro=bairro,
                    numero=numero,
                )
                session.add(cliente)
                session.commit()
                return cliente
        except Exception as e:
            print(f"Erro ao criar cliente: {e}")
            return None

    @cache_query
    def list_by_user(self, user_id: str) -> list[dict[str, Any]]:
        """Lista clientes de um usuário"""
        try:
            with self.db.get_session() as session:
                clientes_query = session.query(Cliente).filter(Cliente.user_id == user_id).all()

                # Converter objetos Cliente para dicionários
                clientes = []
                for cliente in clientes_query:
                    cliente_dict = {
                        "id": cliente.id,
                        "user_id": str(cliente.user_id),
                        "nome": cliente.nome,
                        "cpf": str(cliente.cpf) if cliente.cpf else "",
                        "telefone": str(cliente.telefone) if cliente.telefone else "",
                        "email": cliente.email,
                        "endereco": cliente.endereco,
                        "cidade": cliente.cidade,
                        "estado": cliente.estado,
                        "cep": str(cliente.cep) if cliente.cep else "",
                        "bairro": cliente.bairro,
                        "numero": cliente.numero,
                    }
                    clientes.append(cliente_dict)

                return clientes
        except Exception as e:
            print(f"Erro ao listar clientes: {e}")
            return []

    # Alias para o método traduzido
    listar_por_usuario = list_by_user

    def update(self, cliente_id: int, cliente_data: dict) -> bool:
        """Atualiza os dados de um cliente"""
        try:
            with self.db.get_session() as session:
                cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
                if cliente:
                    for key, value in cliente_data.items():
                        setattr(cliente, key, value)
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Erro ao atualizar cliente: {e}")
            return False

    def delete(self, cliente_id: int) -> bool:
        """Remove um cliente"""
        try:
            with self.db.get_session() as session:
                cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
                if cliente:
                    session.delete(cliente)
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Erro ao deletar cliente: {e}")
            return False

    @cache_query
    def get_by_id(self, cliente_id: int) -> Cliente | None:
        """Busca um cliente pelo ID"""
        try:
            with self.db.get_session() as session:
                return session.query(Cliente).filter(Cliente.id == cliente_id).first()
        except Exception as e:
            print(f"Erro ao buscar cliente: {e}")
            return None
