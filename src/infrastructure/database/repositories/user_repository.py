"""Repositório de usuários"""

from typing import Optional, List, Dict, Any

# from sqlalchemy.orm import Session
# from src.user import login
from ..models.user import User
from ..connections.postgres import postgres
from ..connections.supabase import supabase


class UserRepository:
    """Repositório para operações com usuários"""

    def __init__(self):
        self.db = postgres
        self.supabase = supabase.client

    def create(self, email: str, password: str, nome: str) -> Optional[Dict[str, Any]]:
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
    ) -> Optional[Dict[str, Any]]:
        """Realiza login com email e senha"""
        try:
            response = self.supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            return response
        except Exception as e:
            print(f"Erro no login: {e}")
            return None

    def login_with_otp(self, email: str) -> Optional[Dict[str, Any]]:
        """Envia email com código OTP"""
        try:
            response = self.supabase.auth.sign_in_with_otp({"email": email})
            return response
        except Exception as e:
            print(f"Erro ao enviar OTP: {e}")
            return None

    def get_current_user(self) -> Optional[str]:
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

    def get_modules(self, user_id: str) -> List[Dict[str, Any]]:
        """Obtém os módulos do usuário"""
        try:
            response = (
                self.supabase.table("modulos")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"Erro ao obter módulos: {e}")
            return []

    def get_by_id(self, user_id: str) -> Optional[User]:
        """Busca usuário por ID"""
        with self.db.get_session() as session:
            return session.query(User).filter(User.user_id == user_id).first()

    def list_all(self) -> List[User]:
        """Lista todos os usuários"""
        with self.db.get_session() as session:
            return session.query(User).all()
