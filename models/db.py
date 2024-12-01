"""Base de dados db.py"""

import os
import traceback

from dotenv import load_dotenv
from supabase import Client, create_client

from user import login

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Armazene a chave no .env
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def obter_conexao_supabase() -> Client:
    """Retorna o cliente do Supabase."""
    if not supabase:
        raise ValueError("Cliente Supabase não foi configurado corretamente.")
    return supabase


class Usuario:
    """Classe para gerenciar operações relacionadas a usuários."""

    @staticmethod
    def cadastro_usuario(email: str, senha: str, nome: str) -> bool:
        """Cadastra um novo usuário no Supabase."""
        try:
            # Registrar o usuário no Supabase Auth
            response = supabase.auth.sign_up({"email": email, "password": senha})

            # Verificar se o cadastro foi bem-sucedido
            if not response.user:
                raise ValueError("Erro ao registrar o usuário no Supabase Auth.")

            # Obter o ID do usuário
            user_id = response.user.id

            # Inserir os dados na tabela `usuarios`
            usuario_data = {"user_id": user_id, "nome": nome}
            insert_response = supabase.from_("usuarios").insert(usuario_data).execute()

            # Validar resposta da API
            if insert_response.data is None or len(insert_response.data) == 0:
                raise ValueError(
                    f"Erro na resposta ao inserir na tabela 'usuarios': {insert_response}"
                )

            print("Usuário cadastrado e inserido na tabela 'usuarios' com sucesso!")
            return True

        except ValueError as ve:
            print(f"Erro de validação: {ve}")
            return False

        except Exception as e:  # pylint: disable=broad-except
            print(f"Erro inesperado: {e}")
            print("Detalhes do erro:")
            print(traceback.format_exc())  # Log completo
            return False

    def login_com_otp(email):  # pylint: disable=E0213
        """Envia um e-mail de login com OTP para o usuário."""
        try:
            response = supabase.auth.sign_in_with_otp(credentials=email)
            if response.error:
                print(f"Erro ao enviar e-mail: {response.error.message}")
                return None

            print("E-mail de login enviado com sucesso!")
            return response
        except Exception as e:  # pylint: disable=broad-except
            print(f"Erro ao enviar e-mail: {e}")
            return None

    def login_com_senha(email, password):  # pylint: disable=E0213
        """Faz login de um usuário com e-mail e senha."""
        try:
            response = supabase.auth.sign_in_with_password(
                credentials={"email": email, "password": password}
            )
            print("Login bem-sucedido!")
            return response  # Retorna os dados do usuário e o token
        except Exception as e:  # pylint: disable=broad-except
            print(f"Erro ao fazer login: {e}")
            return None

    def obter_user_id():  # pylint: disable=E0211
        """Obtém o user_id do usuário autenticado."""
        user_response = supabase.auth.get_user()
        if user_response and user_response.user:  # Verifique se o usuário existe
            return user_response.user.id
        return None

    def deslogar(self):  # pylint: disable=E0211
        """Desloga o usuário."""
        supabase.auth.sign_out()
        print("Usuário deslogado com sucesso!")
        login.mostrar_tela(self)


class Cliente:
    """Classe para gerenciar operações relacionadas a clientes."""

    @staticmethod
    def adicionar_cliente(
        user_id,
        nome,
        cpf,
        telefone,
        email,
        endereco,
        cidade,
        estado,
        cep,
        bairro,
        numero,
    ):
        """Adiciona um novo cliente ao banco de dados."""
        try:
            response = (
                supabase.table("clientes")
                .insert(
                    {
                        "user_id": user_id,  # Armazenando o user_id do usuário que cadastrou
                        "nome": nome,
                        "cpf": cpf,
                        "telefone": telefone,
                        "email": email,
                        "endereco": endereco,
                        "cidade": cidade,
                        "estado": estado,
                        "cep": cep,
                        "bairro": bairro,
                        "numero": numero,
                    }
                )
                .execute()
            )
            print("Cliente adicionado com sucesso!")
            return response.data
        except Exception as e:  # pylint: disable=broad-except
            print(f"Erro ao adicionar cliente: {e}")
            return None

    @staticmethod
    def listar_clientes(user_id):
        """Listar clientes cadastrados pelo usuário."""
        try:
            response = (
                supabase.table("clientes")
                .select("*")
                .eq("user_id", user_id)  # Filtra pelo user_id
                .execute()
            )
            return response.data
        except Exception as e:  # pylint: disable=W0718
            print(f"Erro ao listar clientes: {e}")
            return []

    @staticmethod
    def atualizar_cliente(cliente_id, cliente_dados):
        """Atualiza os dados de um cliente."""
        try:
            response = (
                supabase.table("clientes")
                .update(cliente_dados)
                .eq("id", cliente_id)
                .execute()
            )
            if response.data:  # Verifica se a atualização retornou dados
                # print(f"Cliente atualizado com sucesso! {response.data}")
                return True
            else:
                print(f"Erro ao atualizar cliente: {response}")
                return False
        except Exception as e:  # pylint: disable=W0718
            print(f"Erro ao atualizar cliente: {e}")
            return False

    @staticmethod
    def deletar_cliente(cliente_id):
        """Deleta um cliente pelo ID."""
        try:
            response = (
                supabase.table("clientes").delete().eq("id", cliente_id).execute()
            )
            if response.data:  # Verifica se a exclusão retornou dados
                print("Cliente deletado com sucesso!")
                return True
            else:
                print(f"Erro ao deletar cliente: {response}")
                return False
        except Exception as e:  # pylint: disable=W0718
            print(f"Erro ao deletar cliente: {e}")
            return False


def acessar_dados_protegidos():
    """Exemplo de como acessar dados protegidos após o login."""
    # Aqui você pode acessar dados que requerem autenticação
    try:
        # Acesso a dados que requerem autenticação
        response = supabase.from_("sua_tabela").select("*").execute()
        print("Dados:", response.data)
        return response.data
    except Exception as e:  # pylint: disable=broad-except
        print(f"Erro ao acessar dados: {e}")
        return None
