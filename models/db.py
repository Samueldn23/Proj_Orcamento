"""Base de dados db.py"""

import os

from dotenv import load_dotenv

from supabase import Client, create_client

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


# Configurações do Supabase
SUPABASE_URL = "https://whccjbodlnfmublrssmq.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Armazene a chave no .env
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def obter_supabase_client():
    """Retorna o cliente do Supabase."""
    return supabase


class Usuario:
    """Classe para gerenciar operações relacionadas a usuários."""

    def cadastro_usuario(email, senha):  # pylint: disable=E0213
        """Método para cadastrar um novo usuário"""
        try:
            # Chamada para criar um novo usuário
            response = supabase.auth.sign_up({"email": email, "password": senha})

            # Verifica se houve erro
            if response.get("error"):
                print(f"Erro ao cadastrar usuário: {response['error']['message']}")
                return False

            print("Usuário cadastrado com sucesso!")
            return True

        except Exception as e:  # pylint: disable=W0718
            print(f"Erro: {str(e)}")
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


class Cliente:
    """Classe para gerenciar operações relacionadas a clientes."""

    def adicionar_cliente(
        nome, cpf, telefone, email, endereco, cidade, estado, cep, bairro, numero
    ):  # pylint: disable=E0213
        """Adiciona um novo cliente ao banco de dados."""
        try:
            response = (
                supabase.table("clientes")
                .insert(
                    {
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
