from sqlalchemy import Column, Integer, String, create_engine, exc
from sqlalchemy.orm import declarative_base, sessionmaker

# Definir o modelo de base
Base = declarative_base()


# Modelo de usuário
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)


# Criar a engine de banco de dados e a sessão
DATABASE_URL = "sqlite:///app.db"  # Caminho para o banco
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


# Função para criar as tabelas
def criar_tabelas():
    Base.metadata.create_all(bind=engine)


# Função para cadastrar um novo usuário
def cadastrar_usuario(nome, email, senha):
    session = SessionLocal()
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


def autenticar_usuario(email, senha):
    session = SessionLocal()
    try:
        usuario = session.query(Usuario).filter_by(email=email, senha=senha).first()
        return usuario is not None
    finally:
        session.close()
