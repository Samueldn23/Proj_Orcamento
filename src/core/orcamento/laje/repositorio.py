"""Módulo de acesso a dados para lajes."""

from sqlalchemy.orm import Session

from src.infrastructure.database.models.construcoes import Lajes as LajeModel

from .modelo import Laje


class RepositorioLaje:
    """Repositório para operações de laje no banco de dados"""

    def __init__(self, session: Session):
        self.session = session

    def criar(self, laje: Laje) -> Laje:
        """Cria uma nova laje no banco"""
        db_laje = LajeModel(
            projeto_id=laje.projeto_id,
            comprimento=laje.comprimento,
            largura=laje.largura,
            espessura=laje.espessura,
            valor_m3=laje.valor_m3,
            custo_total=laje.custo_total,
            tipo_laje=laje.tipo_laje.name,
            volume=laje.volume,
        )
        self.session.add(db_laje)
        self.session.commit()
        self.session.refresh(db_laje)
        return self._to_domain(db_laje)

    def obter_por_id(self, laje_id: int) -> Laje | None:
        """Busca uma laje pelo ID"""
        if laje := self.session.query(LajeModel).filter_by(id=laje_id).first():
            return self._to_domain(laje)
        return None

    def listar_por_projeto(self, projeto_id: int) -> list[Laje]:
        """Lista todas as lajes de um projeto"""
        return [self._to_domain(laje) for laje in self.session.query(LajeModel).filter_by(projeto_id=projeto_id).all()]

    def atualizar(self, laje: Laje) -> Laje:
        """Atualiza uma laje existente"""
        db_laje = self.session.query(LajeModel).filter_by(id=laje.id).first()
        if not db_laje:
            raise ValueError(f"Laje não encontrada: {laje.id}")

        for attr in ["comprimento", "largura", "espessura", "valor_m3", "custo_total", "tipo_laje", "volume"]:
            if hasattr(laje, attr):
                setattr(db_laje, attr, getattr(laje, attr))

        self.session.commit()
        self.session.refresh(db_laje)
        return self._to_domain(db_laje)

    def excluir(self, laje_id: int) -> bool:
        """Exclui uma laje pelo ID"""
        db_laje = self.session.query(LajeModel).filter_by(id=laje_id).first()
        if db_laje:
            self.session.delete(db_laje)
            self.session.commit()
            return True
        return False

    def _to_domain(self, db_laje: LajeModel) -> Laje:
        """Converte modelo do banco para modelo de domínio"""
        return Laje(
            id=db_laje.id,
            projeto_id=db_laje.projeto_id,
            comprimento=db_laje.comprimento,
            largura=db_laje.largura,
            espessura=db_laje.espessura,
            valor_m3=db_laje.valor_m3,
            custo_total=db_laje.custo_total,
            tipo_laje=db_laje.tipo_laje,
            volume=db_laje.volume,
        )
