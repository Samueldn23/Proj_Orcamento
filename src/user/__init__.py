"""Módulo de usuários"""

from src.infrastructure.database.models import Modulo
from src.infrastructure.database.models.usuarios import Usuario as UsuarioModel
from src.infrastructure.database.repositories import RepositorioUsuario

repositorio_usuario = RepositorioUsuario()


def cadastrar_usuario(nome: str, email: str, senha: str) -> dict | None:
    """Cadastra um novo usuário"""
    try:
        resultado = repositorio_usuario.criar(email, senha, nome)
        return resultado
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")
        return None


class Usuario:
    """Classe para operações de usuários"""

    @staticmethod
    def obter_usuario_atual() -> str | None:
        """Obtém o ID do usuário atual"""
        return repositorio_usuario.obter_usuario_atual()

    @staticmethod
    def obter_por_id(usuario_id: str) -> UsuarioModel | None:
        """Busca usuário por ID"""
        return repositorio_usuario.obter_por_id(usuario_id)

    @staticmethod
    def obter_email_usuario() -> str | None:
        """Obtém o email do usuário atual"""
        return repositorio_usuario.obter_email_usuario()

    @staticmethod
    def obter_modulos(usuario_id: str) -> Modulo | None:
        """Obtém os módulos do usuário"""
        return repositorio_usuario.obter_modulos(usuario_id)

    @staticmethod
    def atualizar_modulos(usuario_id: str, dados_modulo: dict) -> bool:
        """Atualiza os módulos do usuário"""
        return repositorio_usuario.atualizar_modulos(usuario_id, dados_modulo)

    @staticmethod
    def sair() -> bool:
        """Realiza o logout do usuário"""
        return repositorio_usuario.logout()

    # Alias para compatibilidade
    buscar_por_id = obter_por_id
