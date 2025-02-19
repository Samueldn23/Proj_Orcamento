"""Repositório de projetos"""

from typing import Optional, List
from ..models.project import Project
from ..connections.postgres import postgres
from ..connections.supabase import supabase


class ProjetoRepository:
    """Repositório para operações com projetos"""

    def __init__(self):
        self.db = postgres
        self.supabase = supabase.client

    def create(
        self,
        nome: str,
        cliente_id: int,
        descricao: str = None,
        custo_estimado: float = None,
    ) -> Optional[Project]:
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

    def get_by_id(self, projeto_id: int) -> Optional[Project]:
        """Busca um projeto pelo ID"""
        try:
            with self.db.get_session() as session:
                return session.query(Project).filter_by(id=projeto_id).first()
        except Exception as e:
            print(f"Erro ao buscar projeto: {e}")
            return None

    def list_by_client(self, cliente_id: int) -> List[Project]:
        """Lista todos os projetos de um cliente ordenados por data de atualização"""
        try:
            with self.db.get_session() as session:
                return (
                    session.query(Project)
                    .filter_by(cliente_id=cliente_id)
                    .order_by(Project.atualizado_em.desc())
                    .all()
                )
        except Exception as e:
            print(f"Erro ao listar projetos do cliente: {e}")
            return []

    def update(
        self,
        projeto_id: int,
        nome: str = None,
        descricao: str = None,
        custo_estimado: float = None,
    ) -> Optional[Project]:
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
                    session.commit()
                return projeto
        except Exception as e:
            print(f"Erro ao atualizar projeto: {e}")
            return None

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
