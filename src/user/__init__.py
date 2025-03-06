"""Módulo de usuários"""

from src.infrastructure.database.models import Module
from src.infrastructure.database.models.user import User
from src.infrastructure.database.repositories import UserRepository

user_repo = UserRepository()


def cadastrar_usuario(nome: str, email: str, senha: str) -> dict | None:
    """Cadastra um novo usuário"""
    try:
        resultado = user_repo.create(email, senha, nome)
        return resultado
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")
        return None


class Usuario:
    """Classe para operações de usuários"""

    @staticmethod
    def obter_usuario_atual() -> str | None:
        """Obtém o ID do usuário atual"""
        return user_repo.get_current_user()

    @staticmethod
    def buscar_por_id(user_id: str) -> User | None:
        """Busca usuário por ID"""
        return user_repo.get_by_id(user_id)

    @staticmethod
    def obter_email_usuario() -> str | None:
        """Obtém o email do usuário atual"""
        return user_repo.get_current_user_email()

    @staticmethod
    def obter_modulos(user_id: str) -> Module | None:
        """Obtém os módulos do usuário"""
        return user_repo.get_modules(user_id)

    @staticmethod
    def atualizar_modulos(user_id: str, module_data: dict) -> bool:
        """Atualiza os módulos do usuário"""
        return user_repo.update_modules(user_id, module_data)

    @staticmethod
    def sair() -> bool:
        """Realiza o logout do usuário"""
        return user_repo.logout()
