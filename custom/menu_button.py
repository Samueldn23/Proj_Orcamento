import flet as ft
from typing import Callable
import custom.button as btn


class MenuButton(ft.ElevatedButton):
    """Classe para personalizar os botões"""

    def __init__(self, text: str, on_click: Callable, icon: str, width: int = 200):
        super().__init__(
            text=text,
            icon=icon,
            on_click=on_click,
            width=width,
            on_hover=self.efeito_hover,  # Referência ao método de hover
        )

    def efeito_hover(self, e):
        """Gerencia o efeito hover nos botões"""
        if e.data == "true":  # Mouse sobre o botão
            e.control.style = ft.ButtonStyle(
                animation_duration=500,
                overlay_color=ft.colors.BLUE_500,
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, ft.colors.BLUE),
                    ft.ControlState.HOVERED: ft.BorderSide(2, ft.colors.BLUE),
                },
            )
        else:  # Mouse saiu do botão
            e.control.style = ft.ButtonStyle(bgcolor=None, shadow_color=None)
        e.control.update()  # Atualiza o controle

    @staticmethod
    def criar_botao_container(page, text, on_click, icon) -> ft.Container:
        """Cria um container para o botão com efeito hover"""
        # Cria o MenuButton
        button = MenuButton(
            text=text,
            on_click=lambda _: on_click(page),
            icon=icon,
        )

        # Cria um container que envolve o botão
        container = ft.Container(
            content=ft.Column(
                controls=[button],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=2,
            border_radius=25,
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            on_hover=lambda e: MenuButton._handle_button_hover(e)  # Chama o método estático
        )

        return container

    @staticmethod
    def _handle_button_hover(e):
        """Gerencia o efeito hover nos containers"""
        if e.data == "true":  # Mouse entrou
            e.control.scale = 1.05
            e.control.shadow = ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_500,
                offset=ft.Offset(0, 0),
            )
        else:  # Mouse saiu
            e.control.scale = 1.0
            e.control.shadow = None
        e.control.update()


def btn_voltar(page):
    """Cria um botão voltar"""
    return MenuButton("Voltar", lambda _: btn.voltar.principal(page), ft.icons.ARROW_BACK)