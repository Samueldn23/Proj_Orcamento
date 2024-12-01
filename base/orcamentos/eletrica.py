"""Módulo para calcular o custo de eletricidade. eletrica.py"""

import flet as ft

from custom.button import Voltar
from custom.styles_utils import get_style_manager

gsm = get_style_manager()


def mostrar_eletrica(page):
    """Função para mostrar a tela de eletricidade."""
    page.controls.clear()
    page.add(ft.Text("Tela de elétrica", size=24))

    ponto_input = ft.TextField(
        label="pontos elétricos",
        keyboard_type=ft.KeyboardType.NUMBER,
        **gsm.input_style,
    )

    valor_ponto_input = ft.TextField(label="Valor cobrado por ponto", **gsm.input_style)

    resultado_text = ft.Text("Custo Total: R$ 0.00", size=18)

    def calcular():
        try:
            ponto = float(ponto_input.value)

            valor_ponto = float(valor_ponto_input.value)
            custo_total = ponto * valor_ponto
            resultado_text.value = f"Custo Total: R$ {custo_total:.2f}"
            page.update()
        except ValueError:
            resultado_text.value = "Por favor, insira valores válidos."
            page.update()

    calcular_button = ft.ElevatedButton(
        text="Calcular", on_click=calcular, **gsm.button_style
    )

    btn_voltar = gsm.create_button(
        text="Voltar",
        on_click=lambda _: Voltar.orcamento(page),
        icon=ft.Icons.ARROW_BACK,
    )

    page.add(
        ponto_input,
        valor_ponto_input,
        calcular_button,
        resultado_text,
        btn_voltar,
    )
    page.update()
