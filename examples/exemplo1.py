# Exemplo de uso com a nova estrutura
import flet as ft
from custom.styles1 import get_styles, get_btn_hover_effects, get_btn_container  # , apply_theme
from custom.button import voltar


class CalculoParedeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.styles = get_styles()
        self.hover_effects = get_btn_hover_effects()

        # Criando os inputs
        self.comprimento_input = ft.TextField(
            label="Comprimento (m)",
            prefix_icon=ft.icons.STRAIGHTEN,
            suffix_text="metros",
            **self.styles["input"],
        )

        self.altura_input = ft.TextField(
            label="Altura (m)",
            prefix_icon=ft.icons.HEIGHT,
            suffix_text="metros",
            **self.styles["input"],
        )

        self.valor_m2_input = ft.TextField(
            label="Valor por m²",
            prefix_icon=ft.icons.ATTACH_MONEY,
            suffix_text="R$",
            **self.styles["input"],
        )

        self.area_text = ft.Text(size=18)
        self.resultado_text = ft.Text(size=18)

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Cálculo de Parede",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE,
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                self.altura_input,
                                self.comprimento_input,
                                self.valor_m2_input,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        **self.styles["container"],
                    ),
                    ft.ElevatedButton(
                        text="Calcular",
                        icon=ft.icons.CALCULATE,
                        # on_click=self.calcular,
                        style=self.styles["button_base"],
                        on_hover=self.hover_effects["default"],
                    ),
                    self.area_text,
                    self.resultado_text,
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="Voltar",
                            icon=ft.icons.ARROW_BACK,
                            style=self.styles["button_base"],
                            on_click=lambda _: voltar.principal(self.page),
                            on_hover=self.hover_effects["warning"],
                        ),
                        on_hover=lambda e: get_btn_container(e, ft.colors.RED_500),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            padding=0,
            alignment=ft.alignment.center,
        )



def mostrar_exemplo(page: ft.Page):
    page.controls.clear()
    exemplo_1 = CalculoParedeView(page)
    page.add(exemplo_1.build())
    page.update
