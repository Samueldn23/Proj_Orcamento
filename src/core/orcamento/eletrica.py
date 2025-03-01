"""Módulo para calcular o custo de eletricidade. eletrica.py"""

import flet as ft

from src.custom.styles_utils import get_style_manager
from src.navigation.router import navegar_orcamento

gsm = get_style_manager()


def mostrar_eletrica(page, cliente):
    """Função para mostrar a tela de eletricidade."""
    page.controls.clear()
    page.add(ft.Text(f"Orçamento de elétrica para {cliente['nome']}", size=24))

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
        on_click=lambda _: navegar_orcamento(page, cliente),
        icon=ft.Icons.ARROW_BACK,
        hover_color=gsm.colors.VOLTAR,
        width=130,
    )

    page.add(
        ponto_input,
        valor_ponto_input,
        calcular_button,
        resultado_text,
        btn_voltar,
    )
    page.update()
