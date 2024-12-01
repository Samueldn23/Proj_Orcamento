"""Modulo para a tela de empresa."""

import flet as ft

from custom.button import Voltar
from custom.styles_utils import get_style_manager

gsm = get_style_manager()


def tela_empresa(page: ft.Page):
    """Tela de empresa."""
    page.controls.clear()
    page.add(
        gsm.create_button(
            text="Voltar",
            on_click=lambda _: Voltar.principal(page),
            icon=ft.Icons.ARROW_BACK,
        )
    )
