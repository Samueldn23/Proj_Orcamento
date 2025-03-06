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
                    # Log para debug
                    print(f"Repository - Atualizando projeto {projeto_id}")
                    print(f"Valores recebidos: nome='{nome}', descricao='{descricao}', tipo descricao={type(descricao)}")
                    print(f"Valores atuais: nome='{projeto.nome}', descricao='{projeto.descricao}'")

                    # Atualizar nome se não for None (mesmo que seja string vazia)
                    if nome is not None:
                        projeto.nome = nome
                        print(f"Nome atualizado para: '{nome}'")

                    # Atualizar descrição - pode ser None ou string (mesmo vazia)
                    # descricao is None significa que o campo deve ser NULL no banco
                    # descricao = "" significa que o campo deve ser uma string vazia no banco
                    projeto.descricao = descricao
                    print(f"Descrição atualizada para: '{descricao}', tipo={type(descricao)}")

                    # Atualizar custo estimado se não for None
                    if custo_estimado is not None:
                        projeto.custo_estimado = custo_estimado

                    # Atualizar valor total se não for None
                    if valor_total is not None:
                        projeto.valor_total = valor_total

                    # Commit das alterações
                    session.commit()

                    # Recarrega o objeto do banco para confirmar as mudanças
                    session.refresh(projeto)
                    print(f"Após commit: nome='{projeto.nome}', descricao='{projeto.descricao}', tipo descricao={type(projeto.descricao)}")

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
                    print(f"Atualizando apenas valor total: {valor_total} para projeto {projeto_id}")
                    print(f"Valores antes: nome='{projeto.nome}', descricao='{projeto.descricao}'")

                    # Atualiza apenas o valor total e o custo estimado
                    projeto.valor_total = valor_total
                    projeto.custo_estimado = valor_total  # Atualiza também o custo estimado

                    # Commit das alterações
                    session.commit()

                    # Verifica os valores após o commit
                    session.refresh(projeto)
                    print(f"Valores após: nome='{projeto.nome}', descricao='{projeto.descricao}'")

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
