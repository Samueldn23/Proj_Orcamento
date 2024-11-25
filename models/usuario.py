"""Um módulo para gerenciar o cadastro de usuários. usuario.py"""

from sqlalchemy import exc

from models.db import Session
from models.tabelas import Usuario


# Função para cadastrar um novo usuário
def cadastro(nome, email, senha):
    """metodo para cadastrar um novo usuário"""
    session = Session()
    try:
        print(f"Verificando se o e-mail {email} já está registrado...")
        usuario_existente = session.query(Usuario).filter_by(email=email).first()

        if usuario_existente:
            print(f"O e-mail {email} já está registrado.")
            return False

        print(f"Inserindo o usuário {nome} no banco de dados...")
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        session.add(novo_usuario)
        session.commit()
        print(f"Usuário {nome} cadastrado com sucesso!")
        return True

    except exc.SQLAlchemyError as e:
        session.rollback()
        print(f"Erro ao cadastrar usuário: {str(e)}")
        return False

    finally:
        session.close()  # Fechar a sessão


def autenticar(email, senha):
    """metodo para autenticar um usuário"""
    session = Session()
    try:
        usuario = session.query(Usuario).filter_by(email=email, senha=senha).first()
        return usuario is not None
    finally:
        session.close()
