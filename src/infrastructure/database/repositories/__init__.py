"""Módulo de repositórios"""

from .client_repository import ClientRepository as RepositorioCliente
from .module_repository import ModuleRepository as RepositorioModulo
from .projeto_repository import ProjetoRepository as RepositorioProjeto
from .user_repository import RepositorioUsuario

__all__ = [
    "RepositorioCliente",
    "RepositorioModulo",
    "RepositorioProjeto",
    "RepositorioUsuario",
]
