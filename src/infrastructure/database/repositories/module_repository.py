"""Repositório de módulos"""

from typing import Any, Optional  # noqa: F401

from ..connections.postgres import postgres
from ..models.modulos import Modulo


class ModuleRepository:
    """Repositório para operações com módulos"""

    def __init__(self):
        self.db = postgres

    def get_modules(self, user_id: str) -> list[dict[str, Any]]:
        """Obtém os módulos do usuário"""
        try:
            with self.db.get_session() as session:
                modules = session.query(Modulo).filter(Modulo.user_id == user_id).all()

                # Converter objetos Module para dicionários
                result = []
                for module in modules:
                    module_dict = {
                        "id": module.id,
                        "user_id": str(module.user_id),
                        "nome_usuario": module.nome_usuario,
                        "parede": module.parede,
                        "contrapiso": module.contrapiso,
                        "eletrica": module.eletrica,
                        "fundacao": module.fundacao,
                        "laje": module.laje,
                        "telhado": module.telhado,
                    }
                    result.append(module_dict)

                return result
        except Exception as e:
            print(f"Erro ao obter módulos: {e}")
            return []

    def create_default_modules(self, user_id: str, nome_usuario: str) -> bool:
        """Cria os módulos padrão para um novo usuário"""
        try:
            with self.db.get_session() as session:
                module = Modulo(
                    user_id=user_id, nome_usuario=nome_usuario, parede=True, contrapiso=False, eletrica=False, fundacao=False, laje=False, telhado=False
                )
                session.add(module)
                session.commit()
                return True
        except Exception as e:
            print(f"Erro ao criar módulos: {e}")
            return False

    def update_module(self, user_id: str, module_data: dict) -> bool:
        """Atualiza os módulos de um usuário"""
        try:
            with self.db.get_session() as session:
                module = session.query(Modulo).filter(Modulo.user_id == user_id).first()
                if module:
                    for key, value in module_data.items():
                        if hasattr(module, key):
                            setattr(module, key, value)
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Erro ao atualizar módulos: {e}")
            return False
