"""Exemplos de uso do sistema. exemplos.py"""

import flet as ft

from custom.button import Voltar
from custom.styles_utils import get_style_manager

gsm = get_style_manager()


def main(page):
    """Função principal do programa."""
    page.controls.clear()
    page.add(ft.Text("orçamento da laje", size=24))

    comprimento_input = ft.TextField(label="Comprimento (m)", **gsm.input_style)
    largura_input = ft.TextField(label="Largura (m)", **gsm.input_style)
    espessura_input = ft.TextField(label="Espessura (cm)", **gsm.input_style)
    valor_m3_input = ft.TextField(label="Valor por (m³)", **gsm.input_style)

    resultado_text = ft.Text("Custo Total: R$ 0.00", size=18)

    switch = ft.Switch(
        label="cm para mm",
        on_change=lambda e: atualizar(page),
        value=False,
    )
    dd = ft.Dropdown(
        width=100,
        height=50,
        border_color="white",
        text_size=15,
        options=[
            ft.dropdown.Option("cm"),
            ft.dropdown.Option("mm"),
        ],
        value="cm",
    )
    cg = ft.RadioGroup(
        content=ft.Row(
            controls=[
                ft.Radio(
                    value="cm",
                    label="cm",
                    label_position=ft.LabelPosition.LEFT,
                    fill_color="white",
                ),
                ft.Radio(
                    value="mm",
                    label="mm",
                    label_position=ft.LabelPosition.LEFT,
                    fill_color="blue",
                ),
            ],
        ),
        value="cm",
        on_change=lambda e: atualizar(page),
    )

    def atualizar(page):
        if cg.value == "mm":
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

    calcular_button = ft.ElevatedButton(text="Calcular", on_click=calcular)

    btn_voltar2 = gsm.create_button(
        text="Voltar Página Inicial",
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda _: Voltar.principal(page),
        hover_color=gsm.colors.VOLTAR,
        width=220,
    )

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    comprimento_input,
                    # largura_input,
                    # espessura_input,
                    # valor_m3_input,
                    switch,
                    dd,
                    cg,
                ],
                alignment="center",
                spacing=10,  # Espaçamento entre os botões
            ),
            **gsm.container_style,
        ),
    )

    page.add(
        calcular_button,
        resultado_text,
        btn_voltar2,
    )
    page.update()
