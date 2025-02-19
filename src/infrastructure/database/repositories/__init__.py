"""Módulo de repositórios"""

from .user_repository import UserRepository
from .client_repository import ClientRepository
from .projeto_repository import ProjetoRepository
from .module_repository import ModuleRepository

__all__ = [
    "UserRepository",
    "ClientRepository",
    "ProjetoRepository",
    "ModuleRepository",
]
