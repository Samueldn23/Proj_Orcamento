"""Módulo de SPDA (Sistema de Proteção contra Descargas Atmosféricas)"""

from .models import Edificacao, Inspecao, ItemInspecao
from .relatorio import gerar_relatorio
from .SPDA import mostrar_inspecao, salvar_inspecao

__all__ = [
    "Edificacao",
    "Inspecao",
    "ItemInspecao",
    "gerar_relatorio",
    "mostrar_inspecao",
    "salvar_inspecao",
]
