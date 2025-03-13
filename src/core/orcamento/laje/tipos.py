"""Módulo com tipos e constantes para lajes."""

from enum import Enum

# Constantes
CM_TO_M = 0.01
MIN_COMPRIMENTO = 1.0
MAX_COMPRIMENTO = 50.0
MIN_LARGURA = 1.0
MAX_LARGURA = 50.0
MIN_ESPESSURA = 1.0
MAX_ESPESSURA = 50.0
MIN_VALOR_M3 = 1.0
MAX_VALOR_M3 = 10000.0


class TipoLaje(Enum):
    """Tipos de laje suportados"""

    MACICA = "Laje Maciça"
    NERVURADA = "Laje Nervurada"
    PRE_MOLDADA = "Laje Pré-Moldada"

    @property
    def densidade(self) -> float:
        """Retorna a densidade do tipo de laje em kg/m³"""
        _densidades = {TipoLaje.MACICA: 2500, TipoLaje.NERVURADA: 1800, TipoLaje.PRE_MOLDADA: 1600}
        return _densidades[self]
