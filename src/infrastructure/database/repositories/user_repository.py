"""Repositório de usuários"""

from typing import Any

# from sqlalchemy.orm import Session
# from src.user import login
from ...cache.cache_config import cache_query
from ..connections.postgres import postgres
from ..connections.supabase import supabase
from ..models import Module
from ..models.user import User


class UserRepository:
    """Repositório para operações com usuários"""

    def __init__(self):
        self.db = postgres
        self.supabase = supabase.client

    def create(self, email: str, password: str, nome: str) -> dict[str, Any] | None:
        """Cadastra um novo usuário"""
        try:
            # Registrar no Supabase Auth
            auth_response = self.supabase.auth.sign_up(
                {"email": email, "password": password}
            )

            if not auth_response.user:
                raise ValueError("Erro ao registrar usuário no Supabase Auth")

            user_id = auth_response.user.id

            # Criar usuário no banco
            with self.db.get_session() as session:
                user = User(
                    user_id=user_id,
                    nome=nome,
                )
                session.add(user)
                session.commit()

                # Criar módulos padrão
                self.create_default_modules(user_id, nome)

                return {"user": user, "auth_data": auth_response}

        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return None

    def create_default_modules(self, user_id: str, user_name: str) -> bool:
        """Cria os módulos padrão para um novo usuário"""
        try:
            response = (
                self.supabase.table("modulos")
                .insert(
                    {
                        "user_id": user_id,
                        "user_name": user_name,
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

    def login_with_password(
        self, email: str, password: str
    ) -> dict[str, Any] | None:
        """Realiza login com email e senha"""
        try:
            response = self.supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
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
    def get_current_user(self) -> str | None:
        """Obtém o ID do usuário atual"""
        try:
            response = self.supabase.auth.get_user()
            if response and response.user:
                return response.user.id
            return None
        except Exception as e:
            print(f"Erro ao obter usuário atual: {e}")
            return None

    def logout(self) -> bool:
        """Realiza o logout do usuário"""
        try:
            self.supabase.auth.sign_out()
            return True
        except Exception as e:
            print(f"Erro ao realizar logout: {e}")
            return False

    def get_modules(self, user_id: str) -> Module | None:
        """Obtém os módulos do usuário"""
        try:
            with self.db.get_session() as session:
                return session.query(Module).filter(Module.user_id == user_id).first()
        except Exception as e:
            print(f"Erro ao obter módulos: {e}")
            return None

    def update_modules(self, user_id: str, module_data: dict) -> bool:
        """Atualiza os módulos do usuário"""
        try:
            with self.db.get_session() as session:
                modules = (
                    session.query(Module).filter(Module.user_id == user_id).first()
                )
                if modules:
                    for key, value in module_data.items():
                        setattr(modules, key, value)
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Erro ao atualizar módulos: {e}")
            return False

    @cache_query
    def get_by_id(self, user_id: str) -> User | None:
        """Busca usuário por ID"""
        with self.db.get_session() as session:
            return session.query(User).filter(User.user_id == user_id).first()

    @cache_query
    def list_all(self) -> list[User]:
        """Lista todos os usuários"""
        with self.db.get_session() as session:
            return session.query(User).all()
