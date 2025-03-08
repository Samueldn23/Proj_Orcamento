"""Módulo para o cálculo de orçamento de lajes."""

import locale
from enum import Enum

import flet as ft

from src.core.projeto.detalhes_projeto import atualizar_custo_estimado
from src.custom.styles_utils import get_style_manager
from src.infrastructure.database.connections import Session
from src.infrastructure.database.models.construcoes import Lajes
from src.navigation.router import navegar_orcamento

# Configurações
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
gsm = get_style_manager()
session = Session()

# Constantes
CM_TO_M = 0.01
MIN_COMPRIMENTO = 1.0  # Comprimento mínimo em metros
MAX_COMPRIMENTO = 20.0  # Comprimento máximo em metros
MIN_LARGURA = 1.0  # Largura mínima em metros
MAX_LARGURA = 20.0  # Largura máxima em metros
MIN_ESPESSURA = 5.0  # Espessura mínima em centímetros
MAX_ESPESSURA = 50.0  # Espessura máxima em centímetros
MIN_VALOR_M3 = 100.0  # Valor mínimo por m³ em reais
MAX_VALOR_M3 = 10000.0  # Valor máximo por m³ em reais


class TipoLaje(Enum):
    """Enum para representar os tipos de laje."""

    MACICA = "Laje Maciça"
    NERVURADA = "Laje Nervurada"
    PRE_MOLDADA = "Laje Pré-Moldada"


class LajeCalculator:
    """Classe para cálculo de orçamento de lajes"""

    def __init__(self, page: ft.Page, cliente, projeto):
        self.page = page
        self.cliente = cliente
        self.projeto = projeto
        self.resultado_text: ft.Text | None = None
        self._init_controls()

    def _init_controls(self):
        """Inicializa os controles da página"""
        self.comprimento_input = ft.TextField(
            label="Comprimento (m)",
            prefix_icon=ft.Icons.STRAIGHTEN,
            suffix_text="metros",
            keyboard_type=ft.KeyboardType.NUMBER,
            **gsm.input_style,
        )

        self.largura_input = ft.TextField(
            label="Largura (m)",
            prefix_icon=ft.Icons.STRAIGHTEN,
            suffix_text="metros",
            keyboard_type=ft.KeyboardType.NUMBER,
            **gsm.input_style,
        )

        self.espessura_input = ft.TextField(
            label="Espessura (cm)",
            prefix_icon=ft.Icons.HEIGHT,
            suffix_text="centímetros",
            keyboard_type=ft.KeyboardType.NUMBER,
            **gsm.input_style,
        )

        self.valor_m3_input = ft.TextField(
            label="Valor por m³",
            prefix_icon=ft.Icons.ATTACH_MONEY,
            suffix_text="R$",
            keyboard_type=ft.KeyboardType.NUMBER,
            **gsm.input_style,
        )

        self.tipo_laje_dropdown = ft.Dropdown(
            label="Tipo de Laje",
            options=[ft.dropdown.Option(key=tipo.name, text=tipo.value) for tipo in TipoLaje],
            **gsm.input_style,
        )

        self.resultado_text = ft.Text(
            size=18,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

    def _validate_inputs(self) -> tuple[bool, str]:
        """Valida os inputs do formulário"""
        try:
            comprimento = float(self.comprimento_input.value or 0)
            largura = float(self.largura_input.value or 0)
            espessura = float(self.espessura_input.value or 0)
            valor_m3 = float(self.valor_m3_input.value or 0)

            if comprimento <= 0 or largura <= 0 or espessura <= 0 or valor_m3 <= 0:
                return False, "Todos os valores devem ser maiores que zero!"

            if comprimento < MIN_COMPRIMENTO or comprimento > MAX_COMPRIMENTO:
                return False, f"O comprimento deve estar entre {MIN_COMPRIMENTO} e {MAX_COMPRIMENTO} metros!"

            if largura < MIN_LARGURA or largura > MAX_LARGURA:
                return False, f"A largura deve estar entre {MIN_LARGURA} e {MAX_LARGURA} metros!"

            if espessura < MIN_ESPESSURA or espessura > MAX_ESPESSURA:
                return False, f"A espessura deve estar entre {MIN_ESPESSURA} e {MAX_ESPESSURA} centímetros!"

            if valor_m3 < MIN_VALOR_M3 or valor_m3 > MAX_VALOR_M3:
                return False, f"O valor por m³ deve estar entre R$ {MIN_VALOR_M3:.2f} e R$ {MAX_VALOR_M3:.2f}!"

            return True, ""
        except ValueError:
            return False, "Por favor, insira apenas números válidos!"

    def _calcular_orcamento(self) -> tuple[float, float]:
        """
        Calcula o volume e o custo total da laje de acordo com o tipo selecionado.
        Retorna uma tupla com o volume em m³ e o custo total em reais.
        """
        comprimento = float(self.comprimento_input.value)
        largura = float(self.largura_input.value)
        espessura = float(self.espessura_input.value) * CM_TO_M
        valor_m3 = float(self.valor_m3_input.value)
        tipo_laje = self.tipo_laje_dropdown.value

        if tipo_laje == TipoLaje.MACICA.name:
            volume = comprimento * largura * espessura
        elif tipo_laje == TipoLaje.NERVURADA.name:
            # Assumindo nervuras a cada 50 cm e espessura da mesa de 5 cm
            area_mesa = comprimento * largura
            area_nervuras = (comprimento / 0.5) * (largura / 0.5) * (espessura - 0.05)
            volume = area_mesa * 0.05 + area_nervuras
        else:  # TipoLaje.PRE_MOLDADA
            # Assumindo placas de 1.25m x 5m e espessura de 12 cm
            num_placas = (comprimento * largura) / (1.25 * 5)
            volume = num_placas * 1.25 * 5 * 0.12

        custo_total = volume * valor_m3

        return volume, custo_total

    def _update_resultado(self, volume: float, custo_total: float):
        """Atualiza o texto de resultado"""
        self.resultado_text.value = f"Volume: {volume:.2f} m³\nCusto Total: {locale.currency(custo_total, grouping=True)}"
        self.page.update()

    def calcular(self, e):
        """Calcula o orçamento da laje"""
        valid, message = self._validate_inputs()
        if not valid:
            self.page.open(ft.SnackBar(content=ft.Text(message), bgcolor=ft.Colors.ERROR))
            return

        volume, custo_total = self._calcular_orcamento()
        self._update_resultado(volume, custo_total)

    def salvar(self, e):
        try:
            # Validar e calcular
            valid, message = self._validate_inputs()
            if not valid:
                self.page.open(ft.SnackBar(content=ft.Text(message), bgcolor=ft.Colors.ERROR))
                return

            volume, custo_total = self._calcular_orcamento()

            # Criar nova laje no banco
            nova_laje = Lajes(
                projeto_id=self.projeto.id,
                comprimento=float(self.comprimento_input.value),
                largura=float(self.largura_input.value),
                espessura=float(self.espessura_input.value),
                volume=volume,
                valor_m3=float(self.valor_m3_input.value),
                custo_total=custo_total,
                tipo_laje=self.tipo_laje_dropdown.value,
            )

            session.add(nova_laje)
            session.commit()

            # Atualizar o custo estimado do projeto
            atualizar_custo_estimado(self.projeto.id)

            # Mostrar mensagem de sucesso
            self.page.open(
                ft.SnackBar(
                    content=ft.Text("Laje salva com sucesso!"),
                    bgcolor=ft.Colors.GREEN,
                )
            )

            # Navegar para detalhes do projeto
            navegar_orcamento(self.page, self.cliente, self.projeto)

        except Exception as error:
            self.page.open(ft.SnackBar(content=ft.Text(f"Erro ao salvar: {error!s}"), bgcolor=ft.Colors.ERROR))
            print(f"Erro ao salvar: {error!s}")

    def build(self):
        """Constrói a interface da página"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Cabeçalho Compacto
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Cálculo de Laje",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE,
                                ),
                                ft.Row(
                                    [
                                        ft.Text(
                                            f"Projeto: {self.projeto.nome}",
                                            size=12,
                                            color=ft.Colors.BLUE_300,
                                        ),
                                        ft.Text(
                                            f"Cliente: {self.cliente['nome']}",
                                            size=12,
                                            color=ft.Colors.BLUE_300,
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ),
                    # Área de Entrada
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Container(
                                            content=self.comprimento_input,
                                            expand=1,
                                        ),
                                        ft.Container(
                                            content=self.largura_input,
                                            expand=1,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                ft.Row(
                                    [
                                        ft.Container(
                                            content=self.espessura_input,
                                            expand=1,
                                        ),
                                        ft.Container(
                                            content=self.valor_m3_input,
                                            expand=1,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                self.tipo_laje_dropdown,
                            ],
                            spacing=10,
                        ),
                        padding=10,
                        border_radius=10,
                    ),
                    # Botão Calcular
                    gsm.create_button(
                        text="Calcular",
                        icon=ft.Icons.CALCULATE,
                        on_click=self.calcular,
                        width=200,
                        hover_color=ft.Colors.BLUE_600,
                    ),
                    # Resultados
                    ft.Container(
                        content=ft.Column(
                            [
                                self.resultado_text,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                            spacing=5,
                        ),
                        padding=10,
                        border_radius=10,
                    ),
                    # Botões de ação
                    ft.Row(
                        [
                            gsm.create_button(
                                text="Salvar",
                                on_click=self.salvar,
                                icon=ft.Icons.SAVE,
                                hover_color=ft.Colors.GREEN_600,
                                width=130,
                            ),
                            gsm.create_button(
                                text="Voltar",
                                on_click=lambda _: navegar_orcamento(self.page, self.cliente, self.projeto),
                                icon=ft.Icons.ARROW_BACK,
                                hover_color=gsm.colors.VOLTAR,
                                width=130,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=10,
        )


def mostrar_laje(page: ft.Page, cliente, projeto):
    """Função helper para mostrar a página de cálculo de laje"""
    page.controls.clear()
    laje_calculator = LajeCalculator(page, cliente, projeto)
    page.add(laje_calculator.build())
    page.update()
