import flet as ft
from typing import List
from dataclasses import dataclass


@dataclass
class MenuConfig:
    logged_in: bool = False


class MenuSuperior:
    def __init__(self):
        self.config = MenuConfig()

    def require_login(self, page: ft.Page) -> bool:
        from user.login import mostrar_tela

        if not self.config.logged_in:
            mostrar_tela(page)
            return False
        return True

    def mostrar_app(self, page: ft.Page) -> None:
        if self.require_login(page):
            # Código para mostrar a página do app
            pass

    def logout(self, page: ft.Page) -> None:
        self.config.logged_in = False
        # Implementar lógica de logout

    def criar_menu_superior(self) -> ft.Pagelet:
        return ft.Pagelet(
            appbar=ft.AppBar(
                leading=ft.Icon(ft.icons.PALETTE),
                leading_width=40,
                title=ft.Text("Sistema de Orçamentos"),
                center_title=False,
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=self._criar_acoes_menu(),
            ),
            content=ft.Container(),
        )

    def _criar_acoes_menu(self) -> List[ft.Control]:
        return [
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.icons.FILTER_3),
            self._criar_menu_popup(),
        ]

    def _criar_menu_popup(self) -> ft.PopupMenuButton:
        return ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text="Configurações"),
                ft.PopupMenuItem(),  # divisor
                ft.PopupMenuItem(text="Modo Escuro", checked=False),
            ]
        )


class MenuSecundario:
    def criar_menu_cupertino(self) -> ft.Pagelet:
        return ft.Pagelet(
            appbar=ft.CupertinoAppBar(
                leading=ft.Icon(ft.icons.PALETTE),
                bgcolor=ft.colors.SURFACE_VARIANT,
                trailing=ft.Icon(ft.icons.WB_SUNNY_OUTLINED),
                middle=ft.Text("Menu Secundário"),
            ),
            content=ft.Container(ft.Column([ft.Text("Conteúdo")], spacing=10)),
        )


class MenuLateral:
    def criar_menu_lateral(self) -> ft.Pagelet:
        def abrir_drawer_lateral(e):
            pagelet.end_drawer.open = True
            pagelet.end_drawer.update()

        pagelet = ft.Pagelet(
            appbar=ft.AppBar(
                title=ft.Text("Menu Lateral"), bgcolor=ft.colors.AMBER_ACCENT
            ),
            content=ft.Text("Conteúdo Principal"),
            bgcolor=ft.colors.AMBER_100,
            bottom_app_bar=self._criar_barra_inferior(),
            end_drawer=self._criar_drawer_lateral(),
            floating_action_button=ft.FloatingActionButton(
                "Abrir", on_click=abrir_drawer_lateral
            ),
            floating_action_button_location=ft.FloatingActionButtonLocation.CENTER_DOCKED,
            height=400,
        )
        return pagelet

    def _criar_barra_inferior(self) -> ft.BottomAppBar:
        return ft.BottomAppBar(
            bgcolor=ft.colors.BLUE,
            shape=ft.NotchShape.CIRCULAR,
            content=ft.Row(
                controls=[
                    ft.IconButton(icon=ft.icons.MENU, icon_color=ft.colors.WHITE),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.icons.SEARCH, icon_color=ft.colors.WHITE),
                    ft.IconButton(icon=ft.icons.FAVORITE, icon_color=ft.colors.WHITE),
                ]
            ),
        )

    def _criar_drawer_lateral(self) -> ft.NavigationDrawer:
        return ft.NavigationDrawer(
            controls=[
                ft.NavigationDrawerDestination(
                    icon=ft.icons.ADD_TO_HOME_SCREEN_SHARP, label="Opção 1"
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.icons.ADD_COMMENT, label="Opção 2"
                ),
            ]
        )


"""
menu_superior = MenuSuperior()
menu_secundario = MenuSecundario()
menu_lateral = MenuLateral()

# Exemplo de uso
pagelet_superior = menu_superior.criar_menu_superior()

"""
