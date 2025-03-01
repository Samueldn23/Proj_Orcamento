"""Módulo de repositórios"""

from .client_repository import ClientRepository
from .module_repository import ModuleRepository
from .projeto_repository import ProjetoRepository
from .user_repository import UserRepository

__all__ = [
    "ClientRepository",
    "ModuleRepository",
    "ProjetoRepository",
    "UserRepository",
]
