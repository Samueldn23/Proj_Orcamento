"""Módulo com as classes de modelo para lajes."""

from dataclasses import dataclass
from decimal import Decimal

from .tipos import TipoLaje


@dataclass
class Laje:
    """Modelo de domínio para laje"""

    comprimento: Decimal
    largura: Decimal
    espessura: Decimal
    valor_m3: Decimal
    tipo_laje: TipoLaje
    volume: Decimal | None = None
    custo_total: Decimal | None = None
    id: int | None = None
    projeto_id: int | None = None

    @property
    def area(self) -> Decimal:
        """Calcula a área da laje"""
        return self.comprimento * self.largura

    def __post_init__(self):
        """Converte valores para Decimal após inicialização"""
        self.comprimento = Decimal(str(self.comprimento))
        self.largura = Decimal(str(self.largura))
        self.espessura = Decimal(str(self.espessura))
        self.valor_m3 = Decimal(str(self.valor_m3))
        if self.volume:
            self.volume = Decimal(str(self.volume))
        if self.custo_total:
            self.custo_total = Decimal(str(self.custo_total))
