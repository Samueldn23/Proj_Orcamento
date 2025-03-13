"""Módulo de serviços para lajes."""

from decimal import Decimal

from .calculo import calcular_custo_laje, calcular_volume_laje
from .modelo import Laje
from .repositorio import RepositorioLaje
from .tipos import TipoLaje


class ServicoLaje:
    """Serviço com regras de negócio para lajes"""

    def __init__(self, repositorio: RepositorioLaje):
        self.repositorio = repositorio

    def criar_laje(self, projeto_id: int, **dados) -> Laje:
        """Cria uma nova laje aplicando todas as regras de negócio"""
        # Valida dimensões
        valid, msg = self.validar_dimensoes(**dados)
        if not valid:
            raise ValueError(msg)

        # Calcula valores
        volume = calcular_volume_laje(**dados)
        custo_total = calcular_custo_laje(volume, dados["valor_m3"])

        # Cria e persiste
        laje = Laje(projeto_id=projeto_id, volume=Decimal(str(volume)), custo_total=Decimal(str(custo_total)), **dados)

        return self.repositorio.criar(laje)

    def validar_dimensoes(self, comprimento: float, largura: float, espessura: float, valor_m3: float) -> tuple[bool, str | None]:
        """Valida as dimensões da laje"""
        from .tipos import MAX_COMPRIMENTO, MAX_ESPESSURA, MAX_LARGURA, MAX_VALOR_M3, MIN_COMPRIMENTO, MIN_ESPESSURA, MIN_LARGURA, MIN_VALOR_M3

        if any(v <= 0 for v in (comprimento, largura, espessura, valor_m3)):
            return False, "Todos os valores devem ser maiores que zero"

        validations = [
            (comprimento, MIN_COMPRIMENTO, MAX_COMPRIMENTO, "comprimento", "metros"),
            (largura, MIN_LARGURA, MAX_LARGURA, "largura", "metros"),
            (espessura, MIN_ESPESSURA, MAX_ESPESSURA, "espessura", "centímetros"),
            (valor_m3, MIN_VALOR_M3, MAX_VALOR_M3, "valor por m³", "reais"),
        ]

        for valor, min_val, max_val, campo, unidade in validations:
            if not min_val <= valor <= max_val:
                return False, f"O {campo} deve estar entre {min_val} e {max_val} {unidade}"

        return True, None

    def excluir_laje(self, laje_id: int, projeto_id: int) -> tuple[bool, str]:
        """Exclui uma laje seguindo as regras de negócio"""
        try:
            if not self.repositorio.excluir(laje_id):
                return False, "Laje não encontrada"

            from src.core.projeto.detalhes_projeto import atualizar_custo_estimado

            atualizar_custo_estimado(projeto_id)
            return True, "Laje excluída com sucesso"

        except Exception as error:
            return False, f"Erro ao excluir laje: {error}"
