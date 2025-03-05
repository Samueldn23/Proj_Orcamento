"""Repositório de projetos"""

from typing import Optional

from ..connections.postgres import postgres
from ..models.project import Project


class ProjetoRepository:
    """Repositório para operações com projetos"""

    def __init__(self):
        self.db = postgres

    def create(
        self,
        nome: str,
        cliente_id: int,
        descricao: Optional["str"] = None,
        custo_estimado: Optional["float"] = None,
    ) -> Project | None:
        """Adiciona um novo projeto"""
        try:
            with self.db.get_session() as session:
                projeto = Project(
                    nome=nome,
                    cliente_id=cliente_id,
                    descricao=descricao,
                    custo_estimado=custo_estimado,
                )
                session.add(projeto)
                session.commit()
                return projeto
        except Exception as e:
            print(f"Erro ao criar projeto: {e}")
            return None

    def get_by_id(self, projeto_id: int) -> Project | None:
        """Busca um projeto pelo ID"""
        try:
            with self.db.get_session() as session:
                return session.query(Project).filter_by(id=projeto_id).first()
        except Exception as e:
            print(f"Erro ao buscar projeto: {e}")
            return None

    def list_by_client(self, cliente_id: int) -> list[Project]:
        """Lista todos os projetos de um cliente ordenados por data de atualização"""
        try:
            with self.db.get_session() as session:
                return session.query(Project).filter_by(cliente_id=cliente_id).order_by(Project.atualizado_em.desc()).all()
        except Exception as e:
            print(f"Erro ao listar projetos do cliente: {e}")
            return []

    def update(
        self,
        projeto_id: int,
        nome: Optional["str"] = None,
        descricao: Optional["str"] = None,
        custo_estimado: Optional["float"] = None,
        valor_total: Optional["float"] = None,  # Adicionando valor_total
    ) -> Project | None:
        """Atualiza um projeto existente"""
        try:
            with self.db.get_session() as session:
                projeto = session.query(Project).filter_by(id=projeto_id).first()
                if projeto:
                    if nome:
                        projeto.nome = nome
                    if descricao:
                        projeto.descricao = descricao
                    if custo_estimado is not None:
                        projeto.custo_estimado = custo_estimado
                    if valor_total is not None:
                        projeto.valor_total = valor_total
                    session.commit()
                return projeto
        except Exception as e:
            print(f"Erro ao atualizar projeto: {e}")
            return None

    def atualizar_valor_total(self, projeto_id: int, valor_total: float) -> bool:
        """Atualiza o valor total do projeto"""
        try:
            with self.db.get_session() as session:
                projeto = session.query(Project).filter_by(id=projeto_id).first()
                if projeto:
                    projeto.valor_total = valor_total
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Erro ao atualizar valor total: {e}")
            return False

    def delete(self, projeto_id: int) -> bool:
        """Remove um projeto"""
        try:
            with self.db.get_session() as session:
                projeto = session.query(Project).filter_by(id=projeto_id).first()
                if projeto:
                    session.delete(projeto)
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Erro ao deletar projeto: {e}")
            return False
