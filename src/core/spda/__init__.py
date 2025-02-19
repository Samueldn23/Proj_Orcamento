"""Módulo de SPDA (Sistema de Proteção contra Descargas Atmosféricas)"""

from .SPDA import mostrar_inspecao, salvar_inspecao
from .relatorio import gerar_relatorio
from .models import Edificacao, Inspecao, ItemInspecao

__all__ = [
    "mostrar_inspecao",
    "salvar_inspecao",
    "gerar_relatorio",
    "Edificacao",
    "Inspecao",
    "ItemInspecao",
]
