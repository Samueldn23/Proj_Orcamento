"""Repositório de projetos"""

from typing import Optional

from ..connections.postgres import postgres
from ..models.projetos import Projeto


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
    ) -> Projeto | None:
        """Adiciona um novo projeto"""
        try:
            with self.db.session_scope() as session:
                projeto = Projeto(
                    nome=nome,
                    cliente_id=cliente_id,
                    descricao=descricao,
                    custo_estimado=custo_estimado,
                )
                session.add(projeto)
                # O commit é feito automaticamente pelo session_scope
                session.flush()  # Para garantir que o projeto receba um ID
                return projeto
        except Exception as e:
            print(f"Erro ao criar projeto: {e}")
            return None

    def get_by_id(self, projeto_id: int) -> Projeto | None:
        """Busca um projeto pelo ID"""
        try:
            with self.db.session_scope() as session:
                projeto = session.query(Projeto).filter_by(id=projeto_id).first()

                if not projeto:
                    return None

                # Forçar o carregamento das propriedades
                _ = projeto.nome
                _ = projeto.descricao
                _ = projeto.valor_total
                _ = projeto.custo_estimado
                _ = projeto.criado_em
                _ = projeto.atualizado_em

                # Criar uma cópia do objeto que não depende da sessão
                projeto_desacoplado = Projeto(
                    nome=projeto.nome,
                    cliente_id=projeto.cliente_id,
                    descricao=projeto.descricao,
                    valor_total=projeto.valor_total,
                    custo_estimado=projeto.custo_estimado,
                )
                projeto_desacoplado.id = projeto.id
                projeto_desacoplado.criado_em = projeto.criado_em
                projeto_desacoplado.atualizado_em = projeto.atualizado_em

                return projeto_desacoplado
        except Exception as e:
            print(f"Erro ao buscar projeto: {e}")
            return None

    def list_by_client(self, cliente_id: int) -> list[Projeto]:
        """Lista todos os projetos de um cliente ordenados por data de atualização"""
        try:
            projetos = []
            with self.db.session_scope() as session:
                # Obter projetos do banco
                projetos = session.query(Projeto).filter_by(cliente_id=cliente_id).order_by(Projeto.atualizado_em.desc()).all()

                # Para cada projeto, garantir que todos os atributos sejam carregados
                for projeto in projetos:
                    # Forçar o carregamento das propriedades
                    _ = projeto.nome
                    _ = projeto.descricao
                    _ = projeto.valor_total
                    _ = projeto.custo_estimado
                    _ = projeto.criado_em
                    _ = projeto.atualizado_em

                # Converter para dicionários
                projetos_dicts = []
                for projeto in projetos:
                    projeto_dict = {
                        "id": projeto.id,
                        "nome": projeto.nome,
                        "descricao": projeto.descricao,
                        "cliente_id": projeto.cliente_id,
                        "valor_total": projeto.valor_total,
                        "custo_estimado": projeto.custo_estimado,
                        "criado_em": projeto.criado_em,
                        "atualizado_em": projeto.atualizado_em,
                    }
                    projetos_dicts.append(projeto_dict)

                # Criar novos objetos Projeto a partir dos dicionários
                projetos = []
                for p_dict in projetos_dicts:
                    p = Projeto(
                        nome=p_dict["nome"],
                        cliente_id=p_dict["cliente_id"],
                        descricao=p_dict["descricao"],
                        valor_total=p_dict["valor_total"],
                        custo_estimado=p_dict["custo_estimado"],
                    )
                    p.id = p_dict["id"]
                    p.criado_em = p_dict["criado_em"]
                    p.atualizado_em = p_dict["atualizado_em"]
                    projetos.append(p)

            return projetos
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
    ) -> Projeto | None:
        """Atualiza um projeto existente"""
        try:
            with self.db.session_scope() as session:
                projeto = session.query(Projeto).filter_by(id=projeto_id).first()
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

                    # O commit é feito automaticamente pelo session_scope
                    session.flush()

                    # Retorna o projeto atualizado
                    return projeto
                return None
        except Exception as e:
            print(f"Erro ao atualizar projeto: {e}")
            return None

    def atualizar_valor_total(self, projeto_id: int, valor_total: float) -> bool:
        """Atualiza o valor total do projeto"""
        try:
            with self.db.session_scope() as session:
                projeto = session.query(Projeto).filter_by(id=projeto_id).first()
                if projeto:
                    print(f"Atualizando apenas valor total: {valor_total} para projeto {projeto_id}")
                    print(f"Valores antes: nome='{projeto.nome}', descricao='{projeto.descricao}'")

                    # Atualiza apenas o valor total e o custo estimado
                    projeto.valor_total = valor_total
                    projeto.custo_estimado = valor_total  # Atualiza também o custo estimado

                    # O commit é feito automaticamente no session_scope
                    # se não houver exceções

                    return True
                return False
        except Exception as e:
            print(f"Erro ao atualizar valor total: {e}")
            return False

    def delete(self, projeto_id: int) -> bool:
        """Remove um projeto"""
        try:
            with self.db.session_scope() as session:
                projeto = session.query(Projeto).filter_by(id=projeto_id).first()
                if projeto:
                    session.delete(projeto)
                    # O commit é feito automaticamente pelo session_scope
                    return True
                return False
        except Exception as e:
            print(f"Erro ao deletar projeto: {e}")
            return False
