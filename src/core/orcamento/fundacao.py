"""Módulo para cálculo de orçamento de fundação. fundacao.py"""

import flet as ft

from src.custom.styles_utils import get_style_manager
from src.navigation.router import navegar_orcamento

gsm = get_style_manager()


def mostrar_fundacao(page, cliente):
    """Função para mostrar a página de cálculo de fundação"""
    page.controls.clear()
    page.add(ft.Text(f"orçamento da fundação para {cliente['nome']}", size=24))

    comprimento_input = ft.TextField(label="Comprimento (m)", **gsm.input_style)
    largura_input = ft.TextField(label="Largura (m)", **gsm.input_style)
    espessura_input = ft.TextField(label="Espessura (cm)", **gsm.input_style)
    valor_m3_input = ft.TextField(label="Valor por (m³)", **gsm.input_style)

    resultado_text = ft.Text("Custo Total: R$ 0.00", size=18)

    switch = ft.Switch(label="cm para mm", on_change=lambda e: atualizar(), value=False)

    def atualizar():
        if switch.value:
            espessura_input.label = "Espessura (mm)"
        else:
            espessura_input.label = "Espessura (cm)"

        page.update()

    def calcular():
        try:
            comprimento = float(comprimento_input.value)
            largura = float(largura_input.value)
            espessura = float(espessura_input.value)
            volor_m3 = float(valor_m3_input.value)

            if not switch.value:
                espessura = espessura / 100

            custo_total = comprimento * largura * espessura * volor_m3
            resultado_text.value = f"Custo Total: R$ {custo_total:.2f}"
            page.update()

        except ValueError:
            resultado_text.value = "Por favor, insira valores válidos."
            page.update()

    calcular_button = ft.ElevatedButton(
        text="Calcular", on_click=calcular, **gsm.button_style
    )
    voltar_button = gsm.create_button(
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
                    espessura_input,
                    valor_m3_input,
                    switch,
                ],
                alignment="center",
                spacing=10,  # Espaçamento entre os botões
            ),
            **gsm.container_style,
        ),
    )

    page.add(calcular_button, resultado_text, voltar_button)
    page.update()
