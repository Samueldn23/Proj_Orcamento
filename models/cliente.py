"""gerenciamento de clientes. cliente.py"""

from models.tabelas import Cliente

from models.db import Base, Session, engine  # pylint: disable=import-error


# Exemplo de criação
def adicionar_cliente(
    nome, email, telefone, cpf, endereco, cidade, estado, cep, bairro, numero
):
    """Adiciona um novo cliente ao banco de dados."""
    session = Session()
    Base.metadata.create_all(bind=engine)
    cliente = Cliente(
        nome=nome,
        email=email,
        telefone=telefone,
        cpf=cpf,
        endereco=endereco,
        cidade=cidade,
        estado=estado,
        cep=cep,
        bairro=bairro,
        numero=numero,
    )
    session.add(cliente)
    session.commit()
    session.close()
