"""Módulo para o cálculo de orçamento de lajes."""

# Este arquivo serve apenas como ponte para o módulo laje/interface.py
# para manter a compatibilidade com o código existente
from src.core.orcamento.laje.interface import mostrar_laje

# Re-exportando a função para manter compatibilidade
__all__ = ["mostrar_laje"]
