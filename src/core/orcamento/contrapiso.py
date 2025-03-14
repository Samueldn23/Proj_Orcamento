"""Modulo para calcular o valor do contrapiso. contrapiso.py"""

import locale

import flet as ft

from src.custom.styles_utils import get_style_manager
from src.navigation.router import navegar_orcamento

gsm = get_style_manager()

# Define a localidade para pt_BR
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


def mostrar_contrapiso(page, cliente):
    """Função para mostrar o calculo do contrapiso."""
    page.controls.clear()

    page.add(ft.Text(f"Orçamento de Contrapiso para {cliente['nome']}", size=24))

    comprimento_input = ft.TextField(
        label="Comprimento (m)",
        **gsm.input_style,
    )
    largura_input = ft.TextField(
        label="Largura (m)",
        **gsm.input_style,
    )
    valor_input = ft.TextField(
        label="Valor do Metro (R$)",
        **gsm.input_style,
    )
    espessura_input = ft.TextField(
        label="Espessura (Cm)",
        visible=False,
        **gsm.input_style,
    )
    resultado_text = ft.Text("Custo Total: R$ 0.00", size=18)

    # Função para calcular o custo
    def calcular():
        try:
            comprimento = float(comprimento_input.value)
            largura = float(largura_input.value)
            valor_m2 = float(valor_input.value)

            if switch.value:  # switch para metros cúbicos
                espessura = float(espessura_input.value)
                calculo_m3 = (
                    largura * comprimento * (espessura / 100)
                )  # Convertendo espessura de cm para metros
                custo_total = calculo_m3 * valor_m2
            else:  # metros quadrados
                calculo_m2 = largura * comprimento
                custo_total = calculo_m2 * valor_m2

            resultado_text.value = (
                f"Custo Total: {locale.currency(custo_total, grouping=True)}"
            )
        except ValueError:
            resultado_text.value = "Por favor, insira valores válidos."
        page.update()

    # Função para atualizar visibilidade do campo de espessura
    def atualizar():
        espessura_input.visible = switch.value
        page.update()

    switch = ft.Switch(
        label="Metro Quadrado para Metro Cúbico", on_change=atualizar, value=False
    )

    calcular_btn = ft.ElevatedButton(
        text="Calcular",
        on_click=calcular,
        **gsm.button_style,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
    )
    voltar_btn = gsm.create_button(
        text="Voltar",
        on_click=lambda _: navegar_orcamento(page, cliente),
        icon=ft.Icons.ARROW_BACK,
        hover_color=gsm.colors.VOLTAR,
        width=130,
    )

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    comprimento_input,
                    largura_input,
                    valor_input,
                    espessura_input,
                    switch,
                    calcular_btn,
                    resultado_text,
                    voltar_btn,
                ],
                alignment="center",
                spacing=10,
            ),
            **gsm.container_style,
        )
    )
    page.update()
