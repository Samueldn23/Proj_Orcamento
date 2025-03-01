"""Módulo de clientes"""

from .atualizar import tela_editar_cliente
from .cadastrar import Cadastro
from .clientes import tela_clientes

__all__ = ["Cadastro", "tela_clientes", "tela_editar_cliente"]
