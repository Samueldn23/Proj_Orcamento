# Exemplo de uso com a nova estrutura
import flet as ft
from custom.styles1 import obter_efeitos_hover_botao, obter_efeito_container , obter_estilos # 
from custom.button import voltar
import custom.menu_button as mbt


class CalculoParedeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.styles = obter_estilos()
        self.hover_effects = obter_efeitos_hover_botao()

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
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="Calcular",
                            icon=ft.icons.CALCULATE,
                            # on_click=self.calcular,
                            style=self.styles["botao_base"],
                            on_hover=self.hover_effects["padrao"],
                        ),
                        on_hover=lambda e: obter_efeito_container(e, ft.colors.BLUE_500),
                    ),
                    mbt.MenuButton(
                        text="Voltar",
                        on_click=lambda _: voltar.principal(self.page),
                        icon=ft.icons.ARROW_BACK,
                    ),
                    mbt.btn_voltar(self.page),
                    self.area_text,
                    self.resultado_text,
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="Voltar",
                            icon=ft.icons.ARROW_BACK,
                            style=self.styles["botao_base"],
                            on_click=lambda _: voltar.principal(self.page),
                            on_hover=self.hover_effects["aviso"],
                        ),
                        on_hover=lambda e: obter_efeito_container(e, ft.colors.RED_500),
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
