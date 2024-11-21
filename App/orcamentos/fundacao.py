import flet as ft
import custom.button as clk
from custom.styles_utils import get_style_manager

gsm = get_style_manager()


def mostrar_fundacao(page):
    page.controls.clear()
    page.add(ft.Text("orçamento da fundação", size=24))

    comprimento_input = ft.TextField(label="Comprimento (m)", **gsm.input_style)
    largura_input = ft.TextField(label="Largura (m)", **gsm.input_style)
    espessura_input = ft.TextField(label="Espessura (cm)", **gsm.input_style)
    valor_m3_input = ft.TextField(label="Valor por (m³)", **gsm.input_style)

        self.resultado_text = ft.Text(
            size=18,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        self.area_text = ft.Text(
            size=16,
            text_align=ft.TextAlign.CENTER,
        )
    
    def _validate_inputs(self) -> tuple[bool,str]:
        """valida os inputs do formulário"""

        try:
            altura = float(self.altura_input.value or 0)
            comprimento = float(self.comprimento_input.value or 0)
            espessura = float (self.espessura_input.value or 0)
            valor_m3 = float(self.valor_m3_input.value or 0)

            if altura <= 0 or comprimento <= 0 or espessura <=0 or valor_m3 <= 0:
                return False, "Todos os valores devem ser maiores que zero!"

            return True, ""
        except ValueError:
            resultado_text.value = "Por favor, insira valores válidos."
            page.update()

    calcular_button = ft.ElevatedButton(
        text="Calcular", on_click=calcular, **gsm.button_style
    )
    voltar_button = gsm.create_button(
        text="Voltar",
        on_click=lambda e: clk.voltar.orcamento(page),
        icon=ft.icons.ARROW_BACK,
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