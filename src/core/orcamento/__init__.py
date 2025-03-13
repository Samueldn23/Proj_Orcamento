"""Pacote para os módulos de orçamento."""

# Importações de submódulos para serem acessíveis via src.core.orcamento

# Garante que os módulos sejam importados de forma correta
from .listar_construcoes import MenuButton, OrcamentoPage
from .paredes import ParedeCalculator
from .service import ProjetoService

__all__ = ["MenuButton", "OrcamentoPage", "ParedeCalculator", "ProjetoService"]
