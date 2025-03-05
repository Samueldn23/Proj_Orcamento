"""Repositório de clientes"""

from typing import Any

from src.infrastructure.cache.cache_config import cache_query

from ..connections.postgres import postgres
from ..models.client import Client


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
    ) -> Client | None:
        """Adiciona um novo cliente"""
        try:
            with self.db.get_session() as session:
                client = Client(
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
                session.add(client)
                session.commit()
                return client
        except Exception as e:
            print(f"Erro ao criar cliente: {e}")
            return None

    @cache_query
    def list_by_user(self, user_id: str) -> list[dict[str, Any]]:
        """Lista clientes de um usuário"""
        try:
            with self.db.get_session() as session:
                clients_query = session.query(Client).filter(Client.user_id == user_id).all()

                # Converter objetos Client para dicionários
                clients = []
                for client in clients_query:
                    client_dict = {
                        "id": client.id,
                        "user_id": str(client.user_id),
                        "nome": client.nome,
                        "cpf": str(client.cpf) if client.cpf else "",
                        "telefone": str(client.telefone) if client.telefone else "",
                        "email": client.email,
                        "endereco": client.endereco,
                        "cidade": client.cidade,
                        "estado": client.estado,
                        "cep": str(client.cep) if client.cep else "",
                        "bairro": client.bairro,
                        "numero": client.numero,
                    }
                    clients.append(client_dict)

                return clients
        except Exception as e:
            print(f"Erro ao listar clientes: {e}")
            return []

    def update(self, client_id: int, client_data: dict) -> bool:
        """Atualiza os dados de um cliente"""
        try:
            with self.db.get_session() as session:
                client = session.query(Client).filter(Client.id == client_id).first()
                if client:
                    for key, value in client_data.items():
                        setattr(client, key, value)
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Erro ao atualizar cliente: {e}")
            return False

    def delete(self, client_id: int) -> bool:
        """Remove um cliente"""
        try:
            with self.db.get_session() as session:
                client = session.query(Client).filter(Client.id == client_id).first()
                if client:
                    session.delete(client)
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Erro ao deletar cliente: {e}")
            return False

    @cache_query
    def get_by_id(self, client_id: int) -> Client | None:
        """Busca um cliente pelo ID"""
        try:
            with self.db.get_session() as session:
                return session.query(Client).filter(Client.id == client_id).first()
        except Exception as e:
            print(f"Erro ao buscar cliente: {e}")
            return None
