import flet as ft
import custom.styles as stl
import custom.button as btn
import locale

# Define a localidade para pt_BR
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


def mostrar_parede(page):
    page.controls.clear()
    page.add(ft.Text("Tela de Parede", size=24))

    altura_input = ft.TextField(label="Altura (m)", **stl.input_style)
    comprimento_input = ft.TextField(label="comprimento (m)", **stl.input_style)
    valor_m2_input = ft.TextField(label="Valor por m²", **stl.input_style)

    resultado_text = ft.Text("Custo Total: R$ 0.00", size=18)

    def calcular(e):
        try:
            altura = float(altura_input.value)
            comprimento = float(comprimento_input.value)
            valor_m2 = float(valor_m2_input.value)

            custo_total = altura * comprimento * valor_m2

            resultado_text.value = (
                f"Custo Total: {locale.currency(custo_total, grouping=True)}"
            )
            page.update()
        except ValueError:
            resultado_text.value = "Por favor, insira valores válidos."
            page.update()

    page.add(
        ft.Container(
            content=ft.Column(
                [altura_input, comprimento_input, valor_m2_input],
                alignment="center",
                spacing=10,  # Espaçamento entre os botões
            ),
            **stl.container_style,
        ),
    )

    calcular_btn = ft.ElevatedButton(
        text="Calcular",
        on_click=calcular,
        **stl.button_style,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
    )
    voltar_btn = ft.ElevatedButton(
        text="Voltar",
        on_click=lambda e: btn.voltar.orcamento(page),
        **stl.button_style_voltar,
    )

    page.add(calcular_btn, resultado_text, voltar_btn)
    page.update()
