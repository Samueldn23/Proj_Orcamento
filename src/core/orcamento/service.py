"""Serviço de orçamentos"""

from decimal import Decimal


class ProjetoService:  # Renomeado de OrcamentoService
    def __init__(self, repository):
        self.repository = repository

    def calcular_orcamento(self, dados: dict) -> Decimal:
        """Calcula o valor total do orçamento"""
        valor_total = Decimal("0.0")

        # Cálculo para cada componente
        if "fundacao" in dados:
            valor_total += self._calcular_fundacao(dados["fundacao"])
        if "paredes" in dados:
            valor_total += self._calcular_paredes(dados["paredes"])
        # ... outros cálculos

        return valor_total

    def _calcular_fundacao(self, dados: dict) -> Decimal:
        """Calcula o valor da fundação"""
        volume = (
            Decimal(str(dados["comprimento"]))
            * Decimal(str(dados["largura"]))
            * Decimal(str(dados["espessura"]))
        )
        return volume * Decimal(str(dados["valor_m3"]))

    def salvar_orcamento(self, orcamento: dict) -> bool:
        """Salva o orçamento no banco de dados"""
        try:
            return self.repository.save(orcamento)
        except Exception as e:
            print(f"Erro ao salvar orçamento: {e}")
            return False
