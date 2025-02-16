"""Módulo para cálculo de orçamento de paredes. base/orcamentos/parede.py"""

# pylint: disable=file-ignored
import locale
from typing import List, Optional  # pylint: disable=W0611 # noqa: F401

import flet as ft
# import pandas as pd

from src.navigation import router
from src.custom.styles_utils import get_style_manager


# from models.db import Feedback, Orcamento

# Configuração da localização
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
gsm = get_style_manager()

# Definição de materiais e seus custos por m²
MATERIAIS = {
    "Tinta Acrílica": 25.0,  # custo por m²
    "Revestimento Cerâmico": 50.0,
    "Papel de Parede": 30.0,
}


class ParedeCalculator:
    """Classe para cálculo de orçamento de paredes"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.cliente = None
        self.resultado_text: Optional[ft.Text] = None
        self.material_selecionado = "Tinta Acrílica"  # Material padrão
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

        self.material_dropdown = ft.Dropdown(
            label="Escolha o Material",
            options=[ft.dropdown.Option(name) for name in MATERIAIS],
            on_change=self._on_material_change,
            **gsm.input_style,
        )

        self.valor_m2_input = ft.TextField(
            label="Valor por m²",
            prefix_icon=ft.Icons.ATTACH_MONEY,
            suffix_text="R$",
            keyboard_type=ft.KeyboardType.NUMBER,
            **gsm.input_style,
        )

        self.desconto_input = ft.TextField(
            label="Desconto (%)",
            prefix_icon=ft.Icons.DISCOUNT,
            suffix_text="%",
            keyboard_type=ft.KeyboardType.NUMBER,
            **gsm.input_style,
        )

        self.imposto_input = ft.TextField(
            label="Imposto (%)",
            prefix_icon=ft.Icons.MONEY_OFF,
            suffix_text="%",
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

        self.materiais_text = ft.Text(
            size=16,
            text_align=ft.TextAlign.CENTER,
        )

        self.feedback_input = ft.TextField(
            label="Feedback",
            multiline=True,
            **gsm.input_style,
        )

    def _on_material_change(self, e):
        """Atualiza o material selecionado"""
        self.material_selecionado = e.control.value

    def _validate_inputs(self) -> tuple[bool, str]:
        """Valida os inputs do formulário"""
        try:
            altura = float(self.altura_input.value or 0)
            comprimento = float(self.comprimento_input.value or 0)
            valor_m2 = float(self.valor_m2_input.value or 0)
            desconto = float(self.desconto_input.value or 0)
            imposto = float(self.imposto_input.value or 0)

            if altura <= 0 or comprimento <= 0 or valor_m2 <= 0:
                return False, "Todos os valores devem ser maiores que zero!"

            if desconto < 0 or imposto < 0:
                return False, "Desconto e imposto não podem ser negativos!"

            return True, ""
        except ValueError:
            return False, "Por favor, insira apenas números válidos!"

    def _calcular_orcamento(self) -> tuple[float, float]:
        """Calcula a área e o custo total"""
        altura = float(self.altura_input.value)
        comprimento = float(self.comprimento_input.value)
        valor_m2 = float(self.valor_m2_input.value)
        desconto = float(self.desconto_input.value or 0)
        imposto = float(self.imposto_input.value or 0)

        area = altura * comprimento
        custo_total = area * valor_m2

        # Aplicar desconto e imposto
        custo_total -= custo_total * (desconto / 100)
        custo_total += custo_total * (imposto / 100)

        return area, custo_total

    def _calcular_materiais(self, area: float) -> float:
        """Calcula a quantidade de materiais necessários"""
        custo_material = MATERIAIS[self.material_selecionado]
        quantidade_material = area * custo_material
        return quantidade_material

    def _update_resultado(self, area: float, custo_total: float):
        """Atualiza o texto de resultado"""
        self.area_text.value = f"Área total: {area:.2f} m²"
        self.resultado_text.value = (
            f"Custo Total: {locale.currency(custo_total, grouping=True)}"
        )
        quantidade_material = self._calcular_materiais(area)
        self.materiais_text.value = f"Custo dos Materiais ({self.material_selecionado}): {locale.currency(quantidade_material, grouping=True)}"  # pylint: disable=C0301
        self.page.update()

    def _salvar_orcamento(self, area: float, custo_total: float):
        """Salva o orçamento no banco de dados"""
        pass  # pylint: disable=W0107

    def _gerar_relatorio(self):
        """Gera um relatório em CSV dos orçamentos"""
        pass  # pylint: disable=W0107

    def _salvar_feedback(self):
        """Salva o feedback do usuário no banco de dados"""

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
            self._salvar_orcamento(area, custo_total)  # Salva o orçamento
            self._gerar_relatorio()  # Gera relatório
        except ValueError as e:
            self.resultado_text.value = f"Erro ao calcular: {str(e)}"
            self.area_text.value = ""
            self.page.update()

    def enviar_feedback(self, _):
        """Manipula o evento de envio de feedback"""
        self._salvar_feedback()
        self.feedback_input.value = ""
        self.page.update()

    def build(self):
        """Constrói a interface da página"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Cálculo de Parede para ",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE,
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                self.altura_input,
                                self.comprimento_input,
                                self.material_dropdown,
                                self.valor_m2_input,
                                self.desconto_input,
                                self.imposto_input,
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
                    self.materiais_text,
                    self.feedback_input,
                    ft.ElevatedButton(
                        text="Enviar Feedback",
                        icon=ft.Icons.SEND,
                        on_click=self.enviar_feedback,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        **gsm.button_style,
                    ),
                    ft.AlertDialog(
                        open=False,
                        modal=True,
                        title=ft.Text("Feedback Enviado"),
                        content=ft.Text("Obrigado pelo seu feedback!"),
                        actions=[
                            ft.TextButton(
                                "OK", on_click=lambda _: self.page.close_dialog()
                            )
                        ],
                    ),
                    gsm.create_button(
                        text="Voltar",
                        on_click=lambda _: router.navegar_principal(self.page),
                        icon=ft.Icons.ARROW_BACK,
                        hover_color=gsm.colors.VOLTAR,
                        width=130,
                    ),
                    ft.Divider(),
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
