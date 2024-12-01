"""Módulo para cálculo de orçamento de paredes. parede.py"""

import locale
from typing import Optional

import flet as ft

from custom.button import Voltar
from custom.styles_utils import get_style_manager

gsm = get_style_manager()

# Configuração da localização
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
gsm = get_style_manager()


class ParedeCalculator:
    """Classe para cálculo de orçamento de paredes"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.resultado_text: Optional[ft.Text] = None
        self._init_controls()

    def _init_controls(self):
        """Inicializa os controles da página"""
        self.altura_input = ft.TextField(
            label="Altura (m)",
            prefix_icon=ft.Icons.HEIGHT,
            suffix_text="metros",
            keyboard_type=ft.KeyboardType.NUMBER,
            **gsm.input_style,
        )

        self.comprimento_input = ft.TextField(
            label="Comprimento (m)",
            prefix_icon=ft.Icons.STRAIGHTEN,
            suffix_text="metros",
            keyboard_type=ft.KeyboardType.NUMBER,
            **gsm.input_style,
        )

        self.valor_m2_input = ft.TextField(
            label="Valor por m²",
            prefix_icon=ft.Icons.ATTACH_MONEY,
            suffix_text="R$",
            keyboard_type=ft.KeyboardType.NUMBER,
            **gsm.input_style,
        )

        self.resultado_text = ft.Text(
            size=18,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        self.area_text = ft.Text(
            size=16,
            text_align=ft.TextAlign.CENTER,
        )

    def _validate_inputs(self) -> tuple[bool, str]:
        """Valida os inputs do formulário"""
        try:
            altura = float(self.altura_input.value or 0)
            comprimento = float(self.comprimento_input.value or 0)
            valor_m2 = float(self.valor_m2_input.value or 0)

            if altura <= 0 or comprimento <= 0 or valor_m2 <= 0:
                return False, "Todos os valores devem ser maiores que zero!"

            return True, ""
        except ValueError:
            return False, "Por favor, insira apenas números válidos!"

    def _calcular_orcamento(self) -> tuple[float, float]:
        """Calcula a área e o custo total"""
        altura = float(self.altura_input.value)
        comprimento = float(self.comprimento_input.value)
        valor_m2 = float(self.valor_m2_input.value)

        area = altura * comprimento
        custo_total = area * valor_m2

        return area, custo_total

    def _update_resultado(self, area: float, custo_total: float):
        """Atualiza o texto de resultado"""
        self.area_text.value = f"Área total: {area:.2f} m²"
        self.resultado_text.value = (
            f"Custo Total: {locale.currency(custo_total, grouping=True)}"
        )
        self.page.update()

    def calcular(self, _):
        """Manipula o evento de cálculo"""
        valid, message = self._validate_inputs()
        if not valid:
            self.resultado_text.value = message
            self.area_text.value = ""
            self.page.update()
            return

        try:
            area, custo_total = self._calcular_orcamento()
            self._update_resultado(area, custo_total)
        except ValueError as e:
            self.resultado_text.value = f"Erro ao calcular: {str(e)}"
            self.area_text.value = ""
            self.page.update()

    def build(self):
        """Constrói a interface da página"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Cálculo de Parede",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE,
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
                        **gsm.container_style,
                    ),
                    ft.ElevatedButton(
                        text="Calcular",
                        icon=ft.Icons.CALCULATE,
                        on_click=self.calcular,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        **gsm.button_style,
                    ),
                    self.area_text,
                    self.resultado_text,
                    gsm.create_button(
                        text="Voltar",
                        on_click=lambda _: Voltar.orcamento(self.page),
                        icon=ft.Icons.ARROW_BACK,
                        hover_color=gsm.colors.VOLTAR,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=0,
            alignment=ft.alignment.center,
        )


def mostrar_parede(page: ft.Page):
    """Função helper para mostrar a página de cálculo de parede"""
    page.controls.clear()
    parede_calculator = ParedeCalculator(page)
    page.add(parede_calculator.build())
    page.update()
