"""Repositório de usuários"""

from typing import Any

# from sqlalchemy.orm import Session
# from src.user import login
from ...cache.cache_config import cache_query, clear_cache
from ..connections.postgres import postgres
from ..connections.supabase import supabase
from ..models import Modulo
from ..models.usuarios import Usuario


class RepositorioUsuario:
    """Repositório para operações com usuários"""

    def __init__(self):
        self.db = postgres
        self.supabase = supabase.client

    def criar(self, email: str, senha: str, nome: str) -> dict[str, Any] | None:
        """Cadastra um novo usuário"""
        try:
            # Registrar no Supabase Auth
            auth_response = self.supabase.auth.sign_up({"email": email, "password": senha})

            if not auth_response.user:
                raise ValueError("Erro ao registrar usuário no Supabase Auth")

            user_id = auth_response.user.id

            # Criar usuário no banco
            with self.db.get_session() as sessao:
                usuario = Usuario(
                    user_id=user_id,
                    nome=nome,
                )
                sessao.add(usuario)
                sessao.commit()

                # Criar módulos padrão
                self.criar_modulos_padrao(user_id, nome)

                return {"usuario": usuario, "dados_auth": auth_response}

        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return None

    def criar_modulos_padrao(self, user_id: str, nome_usuario: str) -> bool:
        """Cria os módulos padrão para um novo usuário"""
        try:
            response = (
                self.supabase.table("modulos")
                .insert(
                    {
                        "user_id": user_id,
                        "nome_usuario": nome_usuario,
                        "parede": True,
                        "contrapiso": False,
                        "eletrica": False,
                        "fundacao": False,
                        "laje": False,
                        "telhado": False,
                    }
                )
                .execute()
            )
            return bool(response.data)
        except Exception as e:
            print(f"Erro ao criar módulos: {e}")
            return False

    def login_com_senha(self, email: str, password: str) -> dict[str, Any] | None:
        """Realiza login com email e senha"""
        try:
            response = self.supabase.auth.sign_in_with_password({"email": email, "password": password})
            return response
        except Exception as e:
            print(f"Erro no login: {e}")
            return None

    def login_with_otp(self, email: str) -> dict[str, Any] | None:
        """Envia email com código OTP"""
        try:
            response = self.supabase.auth.sign_in_with_otp({"email": email})
            return response
        except Exception as e:
            print(f"Erro ao enviar OTP: {e}")
            return None

    @cache_query
    def obter_por_id(self, user_id: str) -> Usuario | None:
        """Busca usuário por ID"""
        with self.db.get_session() as sessao:
            return sessao.query(Usuario).filter(Usuario.user_id == user_id).first()

    @cache_query
    def listar_todos(self) -> list[Usuario]:
        """Lista todos os usuários"""
        with self.db.get_session() as sessao:
            return sessao.query(Usuario).all()

    def obter_modulos(self, user_id: str) -> Modulo | None:
        """Obtém os módulos do usuário"""
        try:
            with self.db.get_session() as sessao:
                return sessao.query(Modulo).filter(Modulo.user_id == user_id).first()
        except Exception as e:
            print(f"Erro ao obter módulos: {e}")
            return None

    def atualizar_modulos(self, user_id: str, dados_modulo: dict[str, bool]) -> bool:
        """Atualiza os módulos do usuário"""
        try:
            with self.db.get_session() as sessao:
                modulos = sessao.query(Modulo).filter(Modulo.user_id == user_id).first()
                if modulos:
                    for chave, valor in dados_modulo.items():
                        if hasattr(modulos, chave):
                            setattr(modulos, chave, valor)
                    sessao.commit()
                    return True
                return False
        except Exception as e:
            print(f"Erro ao atualizar módulos: {e}")
            return False

    def logout(self) -> bool:
        """Realiza o logout do usuário"""
        try:
            print("Executando logout no supabase...")

            # Tenta o logout normal
            try:
                self.supabase.auth.sign_out()
                print("Logout do supabase realizado")
            except Exception as e:
                print(f"Aviso no sign_out: {e}")

            # Força a limpeza do cache
            clear_cache()
            print("Cache limpo")

            # Tenta uma nova conexão para garantir que a sessão atual foi descartada
            try:
                # Recria a instância do cliente
                from ..connections.supabase import supabase

                self.supabase = supabase.client
                print("Cliente Supabase reinicializado")
            except Exception as e:
                print(f"Aviso na reinicialização do cliente: {e}")

            return True
        except Exception as e:
            print(f"Erro ao realizar logout: {e}")
            return False

    def atualizar(self, user_id: str, dados: dict[str, Any]) -> bool:
        """Atualiza dados do usuário"""
        try:
            with self.db.get_session() as sessao:
                usuario = sessao.query(Usuario).filter(Usuario.user_id == user_id).first()
                if not usuario:
                    return False

                for chave, valor in dados.items():
                    if hasattr(usuario, chave):
                        setattr(usuario, chave, valor)

                sessao.commit()
                return True
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")
            return False

    def excluir(self, user_id: str) -> bool:
        """Exclui um usuário"""
        try:
            with self.db.get_session() as sessao:
                usuario = sessao.query(Usuario).filter(Usuario.user_id == user_id).first()
                if not usuario:
                    return False

                sessao.delete(usuario)
                sessao.commit()
                return True
        except Exception as e:
            print(f"Erro ao excluir usuário: {e}")
            return False

    def definir_usuario_atual(self, user_id: str) -> None:
        """Define o usuário atual"""
        # ... existing code ...

    def obter_usuario_atual(self) -> str | None:
        """Obtém o ID do usuário atual"""
        try:
            # Tenta obter o usuário autenticado
            usuario = self.supabase.auth.get_user()
            if usuario and usuario.user and usuario.user.id:
                return usuario.user.id
            return None
        except Exception as e:
            print(f"Erro ao obter usuário atual: {e}")
            return None

    def obter_por_email(self, email: str) -> dict[str, Any] | None:
        """Busca usuário por email no Supabase Auth"""
        # ... existing code ...

    def obter_email_usuario(self) -> str | None:
        """Obtém o email do usuário atual através do Supabase Auth"""
        try:
            # Tenta obter o usuário autenticado
            usuario = self.supabase.auth.get_user()
            if usuario and usuario.user and usuario.user.email:
                return usuario.user.email
            return None
        except Exception as e:
            print(f"Erro ao obter email do usuário: {e}")
            return None

    # Alias para método antigo
    get_user_email = obter_email_usuario
