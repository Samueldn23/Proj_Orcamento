"""Implementação de testes para o banco de dados."""

from models.db import Session, criar_tabelas
from models.tabelas import Cliente


# Testar a conexão e inserir um cliente
def testar_conexao(event=None):  # pylint: disable=unused-argument
    """Testa a conexão com o banco de dados e insere um cliente de teste."""
    criar_tabelas()  # Criar tabelas no banco de dados
    session = Session()

    # Inserir um cliente de teste
    cliente_teste = Cliente(
        nome="Teste Supabase",
        cpf="12345678900",
        telefone="61999999999",
        email="teste@supabase.com",
    )
    session.add(cliente_teste)
    session.commit()

    # Consultar clientes
    clientes = session.query(Cliente).all()
    for cliente in clientes:
        print(cliente)

    session.close()


if __name__ == "__main__":
    testar_conexao()
