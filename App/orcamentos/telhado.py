import flet as ft
import custom.button as clk
import locale
from custom.styles_utils import get_style_manager

gsm = get_style_manager()

# Define a localidade para pt_BR
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


def mostrar_telhado(page):
    page.controls.clear()

    page.add(ft.Text("Telhado", size=24))

    comprimento_input = ft.TextField(label="Comprimento (m)", **gsm.input_style)
    largura_input = ft.TextField(
        label="Largura (m)",
        **gsm.input_style,
    )
    valor_input = ft.TextField(
        label="Valor do Metro (R$)",
        **gsm.input_style,
    )
    valor_material_input = ft.TextField(
        label="Valor do material (R$) ",
        visible=False,
        **gsm.input_style,
    )
    resultado_text = ft.Text("Custo Total: R$ 0.00", size=18)

    # Função para calcular o custo
    def calcular(e):
        try:
            comprimento = float(comprimento_input.value)
            largura = float(largura_input.value)
            valor_m2 = float(valor_input.value)

            if switch.value:  # switch para adicionar valor do material
                valor_material = float(valor_material_input.value)
                calculo_m3 = largura * comprimento  # cálculo de área (m²)
                custo_total = calculo_m3 * valor_material
            else:  # cálculo com valor por metro quadrado
                calculo_m2 = largura * comprimento
                custo_total = calculo_m2 * valor_m2

            resultado_text.value = (
                f"Custo Total: {locale.currency(custo_total, grouping=True)}"
            )
        except ValueError:
            resultado_text.value = "Por favor, insira valores válidos."
        page.update()

    # Função para atualizar visibilidade do campo de valor material
    def atualizar(e):
        valor_material_input.visible = switch.value
        page.update()

    switch = ft.Switch(
        label="Adicionar valor do material", on_change=atualizar, value=False
    )

    calcular_btn = ft.ElevatedButton(
        text="Calcular",
        on_click=calcular,
        **gsm.button_style,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
    )
    voltar_btn = gsm.create_button(
        text="Voltar",
        on_click=lambda _: clk.voltar.orcamento(page),
        icon=ft.icons.ARROW_BACK,
        hover_color=gsm.colors.VOLTAR,        
    )

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    comprimento_input,
                    largura_input,
                    valor_input,
                    valor_material_input,
                    switch,
                    calcular_btn,
                    resultado_text,
                    voltar_btn,
                ],
                alignment="center",
                spacing=10,  # Espaçamento entre os controles
            ),
            **gsm.container_style,
        ),
    )
    page.update()
