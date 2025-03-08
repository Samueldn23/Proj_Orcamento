"""Gerenciamento de módulos do sistema"""

import flet as ft

# from src.infrastructure.database.models import Modulo
from src.custom.styles_utils import get_style_manager
from src.infrastructure.database.repositories import RepositorioUsuario

gsm = get_style_manager()
repositorio_usuario = RepositorioUsuario()


class GerenciadorModulos:
    def __init__(self):
        self.switches = {
            "parede": ft.Switch(label="Módulo Parede", value=False),
            "contrapiso": ft.Switch(label="Módulo Contrapiso", value=False),
            "eletrica": ft.Switch(label="Módulo Elétrica", value=False),
            "fundacao": ft.Switch(label="Módulo Fundação", value=False),
            "laje": ft.Switch(label="Módulo Laje", value=False),
            "telhado": ft.Switch(label="Módulo Telhado", value=False),
        }
        self.page = None

    def carregar_modulos(self):
        """Carrega o estado dos módulos do banco de dados"""
        try:
            user_id = repositorio_usuario.obter_usuario_atual()
            if not user_id:
                return False

            modulos = repositorio_usuario.obter_modulos(user_id)
            if modulos:
                # Atualiza os switches com os valores do banco
                self.switches["parede"].value = modulos.parede
                self.switches["contrapiso"].value = modulos.contrapiso
                self.switches["eletrica"].value = modulos.eletrica
                self.switches["fundacao"].value = modulos.fundacao
                self.switches["laje"].value = modulos.laje
                self.switches["telhado"].value = modulos.telhado
                return True
            return False
        except Exception as error:
            print(f"Erro ao carregar módulos: {error}")
            return False

    def salvar_modulos(self, e):
        """Salva o estado dos módulos no banco de dados"""
        try:
            user_id = repositorio_usuario.obter_usuario_atual()
            if not user_id:
                return False

            modulos_data = {
                "parede": self.switches["parede"].value,
                "contrapiso": self.switches["contrapiso"].value,
                "eletrica": self.switches["eletrica"].value,
                "fundacao": self.switches["fundacao"].value,
                "laje": self.switches["laje"].value,
                "telhado": self.switches["telhado"].value,
            }

            success = repositorio_usuario.atualizar_modulos(user_id, modulos_data)

            # Mostra mensagem de sucesso/erro
            if e and e.page:
                e.page.open(
                    ft.SnackBar(
                        content=ft.Text("Módulos salvos com sucesso!" if success else "Erro ao salvar módulos!"),
                        bgcolor=ft.Colors.GREEN if success else ft.Colors.RED,
                    )
                )
                e.page.update()

            return success
        except Exception as error:
            print(f"Erro ao salvar módulos: {error}")
            if e and e.page:
                e.page.open(
                    ft.SnackBar(
                        content=ft.Text(f"Erro ao salvar módulos: {error}"),
                        bgcolor=ft.Colors.RED,
                    )
                )
                e.page.update()
            return False

    def build(self):
        """Constrói a interface dos módulos"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Módulos do Sistema", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            self.switches["parede"],
                            self.switches["contrapiso"],
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        [
                            self.switches["eletrica"],
                            self.switches["fundacao"],
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        [
                            self.switches["laje"],
                            self.switches["telhado"],
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        [
                            gsm.create_button(
                                text="Salvar Módulos",
                                icon=ft.Icons.SAVE,
                                on_click=self.salvar_modulos,
                                hover_color=ft.Colors.GREEN,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=10,
            ),
            padding=20,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
            border_radius=10,
        )
