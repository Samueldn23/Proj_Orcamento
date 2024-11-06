import flet as ft
import custom.styles as stl
import custom.button as btn


def mostrar_fundacao(page):
    page.controls.clear()
    page.add(ft.Text("orçamento da fundação", size=24))

    comprimento_input = ft.TextField(label="Comprimento (m)", **stl.input_style)
    largura_input = ft.TextField(label="Largura (m)", **stl.input_style)
    espessura_input = ft.TextField(label="Espessura (cm)", **stl.input_style)
    valor_m3_input = ft.TextField(label="Valor por (m³)", **stl.input_style)

    resultado_text = ft.Text("Custo Total: R$ 0.00", size=18)

    switch = ft.Switch(
        label="cm para mm", on_change=lambda e: atualizar(page), value=False
    )

    def atualizar(e):
        if switch.value:
            espessura_input.label = "Espessura (mm)"
        else:
            espessura_input.label = "Espessura (cm)"

        page.update()

    def calcular(e):
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
        text="Calcular", on_click=calcular, **stl.button_style
    )
    voltar_button = ft.ElevatedButton(
        text="Voltar",
        on_click=lambda e: btn.voltar.orcamento(page),
        **stl.button_style_voltar,
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
            **stl.container_style,
        ),
    )

    page.add(calcular_button, resultado_text, voltar_button)
    page.update()
