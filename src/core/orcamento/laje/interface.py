"""Módulo de interface para o cálculo de orçamento de lajes."""

import locale
from dataclasses import dataclass
from typing import Any

import flet as ft

from src.core.orcamento.laje.calculo import (
    calcular_custo_laje,
    calcular_materiais_laje,
    calcular_peso_laje,
    calcular_volume_laje,
)
from src.core.orcamento.laje.repositorio import RepositorioLaje
from src.core.orcamento.laje.servico import ServicoLaje

# Atualiza imports para usar o novo módulo tipos
from src.core.orcamento.laje.tipos import (
    MAX_COMPRIMENTO,
    MAX_ESPESSURA,
    MAX_LARGURA,
    MAX_VALOR_M3,
    MIN_COMPRIMENTO,
    MIN_ESPESSURA,
    MIN_LARGURA,
    MIN_VALOR_M3,
    TipoLaje,
)
from src.custom.styles_utils import get_style_manager
from src.infrastructure.database.connections.postgres import postgres
from src.navigation.router import navegar_orcamento

# Configurações
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
gsm = get_style_manager()


@dataclass
class LajeInputs:
    """Classe para armazenar os inputs do formulário de laje"""

    comprimento: float
    largura: float
    espessura: float
    valor_m3: float
    tipo_laje: str

    @classmethod
    def from_form(cls, form: "LajeCalculator") -> "LajeInputs":
        """Cria uma instância a partir dos campos do formulário"""
        return cls(
            comprimento=float(form.comprimento_input.value or 0),
            largura=float(form.largura_input.value or 0),
            espessura=float(form.espessura_input.value or 0),
            valor_m3=float(form.valor_m3_input.value or 0),
            tipo_laje=form.tipo_laje_dropdown.value or TipoLaje.MACICA.name,
        )


class LajeCalculator:
    """Classe para cálculo de orçamento de lajes"""

    def __init__(self, page: ft.Page, cliente: dict[str, Any], projeto: Any):
        self.page = page
        self.cliente = cliente
        self.projeto = projeto
        self.session = postgres.get_session()  # Adiciona sessão do banco
        self._init_controls()

    def _init_controls(self):
        """Inicializa os controles do formulário"""
        self.comprimento_input = self._create_numeric_field("Comprimento (m)", ft.Icons.STRAIGHTEN, "metros")
        self.largura_input = self._create_numeric_field("Largura (m)", ft.Icons.STRAIGHTEN, "metros")
        self.espessura_input = self._create_numeric_field("Espessura (cm)", ft.Icons.HEIGHT, "centímetros")
        self.valor_m3_input = self._create_numeric_field("Valor por m³", ft.Icons.ATTACH_MONEY, "R$")
        self.tipo_laje_dropdown = self._create_tipo_laje_dropdown()
        self.resultado_text = self._create_resultado_text()

    def _create_numeric_field(self, label: str, icon: str, suffix: str) -> ft.TextField:
        """Cria um campo numérico padronizado"""
        return ft.TextField(label=label, prefix_icon=icon, suffix_text=suffix, keyboard_type=ft.KeyboardType.NUMBER, **gsm.input_style)

    def _create_tipo_laje_dropdown(self) -> ft.Dropdown:
        """Cria o dropdown de tipos de laje"""
        return ft.Dropdown(label="Tipo de Laje", options=[ft.dropdown.Option(key=tipo.name, text=tipo.value) for tipo in TipoLaje], **gsm.input_style)

    def _create_resultado_text(self) -> ft.Text:
        """Cria o texto de resultado"""
        return ft.Text(size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    def _validate_inputs(self, inputs: LajeInputs) -> tuple[bool, str]:
        """Valida os inputs do formulário"""
        try:
            if any(v <= 0 for v in (inputs.comprimento, inputs.largura, inputs.espessura, inputs.valor_m3)):
                return False, "Todos os valores devem ser maiores que zero!"

            validations = [
                (inputs.comprimento, MIN_COMPRIMENTO, MAX_COMPRIMENTO, "comprimento", "metros"),
                (inputs.largura, MIN_LARGURA, MAX_LARGURA, "largura", "metros"),
                (inputs.espessura, MIN_ESPESSURA, MAX_ESPESSURA, "espessura", "centímetros"),
                (inputs.valor_m3, MIN_VALOR_M3, MAX_VALOR_M3, "valor por m³", "reais"),
            ]

            for valor, min_val, max_val, campo, unidade in validations:
                if not min_val <= valor <= max_val:
                    return False, f"O {campo} deve estar entre {min_val} e {max_val} {unidade}!"

            return True, ""
        except ValueError:
            return False, "Por favor, insira apenas números válidos!"

    def _calcular_orcamento(self, inputs: LajeInputs) -> tuple[float, float]:
        """Calcula o volume e custo total da laje"""
        volume = calcular_volume_laje(inputs.comprimento, inputs.largura, inputs.espessura, inputs.tipo_laje)
        custo_total = calcular_custo_laje(volume, inputs.valor_m3)
        return volume, custo_total

    def _update_resultado(self, volume: float, custo_total: float, tipo_laje: str):
        """Atualiza o texto de resultado"""
        peso = calcular_peso_laje(volume, tipo_laje)
        materiais = calcular_materiais_laje(volume, tipo_laje)

        resultado = [
            f"Volume: {volume:.2f} m³",
            f"Custo Total: {locale.currency(custo_total, grouping=True)}",
            f"Peso estimado: {peso:.0f} kg",
            "\nMateriais estimados:",
            f"- Aço: {materiais['aco']:.1f} kg",
            f"- Cimento: {materiais['cimento']:.1f} kg",
            f"- Areia: {materiais['areia']:.2f} m³",
            f"- Brita: {materiais['brita']:.2f} m³",
        ]

        self.resultado_text.value = "\n".join(resultado)
        self.page.update()

    def calcular(self, e):  # Remove async pois flet não suporta
        """Calcula o orçamento da laje"""
        try:
            inputs = LajeInputs.from_form(self)
            valid, message = self._validate_inputs(inputs)

            if not valid:
                self.page.open = ft.SnackBar(content=ft.Text(message), bgcolor=ft.Colors.ERROR)
                self.page.open = True
                self.page.update()
                return

            volume, custo_total = self._calcular_orcamento(inputs)
            self._update_resultado(volume, custo_total, inputs.tipo_laje)

        except Exception as error:
            self.page.open = ft.SnackBar(content=ft.Text(f"Erro ao calcular: {error}"), bgcolor=ft.Colors.ERROR)
            self.page.open = True
            self.page.update()

    def _handle_error(self, message: str):
        """Centraliza tratamento de erros"""
        self.page.open = ft.SnackBar(content=ft.Text(message), bgcolor=ft.Colors.ERROR)
        self.page.open = True
        self.page.update()

    def _handle_success(self, message: str):
        """Centraliza mensagens de sucesso"""
        self.page.open = ft.SnackBar(content=ft.Text(message), bgcolor=ft.Colors.GREEN)
        self.page.open = True
        self.page.update()

    def salvar(self, e):
        """Salva a laje com tratamento de erros melhorado"""
        try:
            inputs = LajeInputs.from_form(self)
            if not self._validate_inputs(inputs)[0]:
                return

            self._handle_success("Laje salva com sucesso!")
            navegar_orcamento(self.page, self.cliente, self.projeto)

        except Exception as error:
            self._handle_error(f"Erro ao salvar: {error}")

    def build(self) -> ft.Container:
        """Constrói a interface da página"""
        return ft.Container(
            content=ft.Column([self._build_header(), self._build_form(), self._build_actions()], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            padding=10,
        )

    def _build_header(self) -> ft.Container:
        """Constrói o cabeçalho da página"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Cálculo de Laje", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                    ft.Row(
                        [
                            ft.Text(f"Projeto: {self.projeto.nome}", size=12, color=ft.Colors.BLUE_300),
                            ft.Text(f"Cliente: {self.cliente['nome']}", size=12, color=ft.Colors.BLUE_300),
                        ]
                    ),
                ]
            )
        )

    def _build_form(self) -> ft.Container:
        """Constrói o formulário de entrada"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row([ft.Container(content=self.comprimento_input, expand=1), ft.Container(content=self.largura_input, expand=1)], spacing=10),
                    ft.Row([ft.Container(content=self.espessura_input, expand=1), ft.Container(content=self.valor_m3_input, expand=1)], spacing=10),
                    self.tipo_laje_dropdown,
                    ft.Row(
                        [gsm.create_button(text="Calcular", icon=ft.Icons.CALCULATE, on_click=self.calcular, width=200, hover_color=ft.Colors.BLUE_600)],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [self.resultado_text],
                            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                            spacing=5,
                        ),
                        padding=10,
                        border_radius=10,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=10,
            border_radius=10,
        )

    def _build_actions(self) -> ft.Row:
        """Constrói os botões de ação"""
        return ft.Row(
            [
                gsm.create_button(text="Salvar", on_click=self.salvar, icon=ft.Icons.SAVE, hover_color=ft.Colors.GREEN_600, width=130),
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
        )


def mostrar_laje(page: ft.Page, cliente: dict[str, Any], projeto: Any):  # Remove async
    """Função helper para mostrar a página de cálculo de laje"""
    page.controls.clear()
    laje_calculator = LajeCalculator(page, cliente, projeto)
    page.add(laje_calculator.build())
    page.update()


def excluir_laje(page: ft.Page, laje_id: int, projeto_id: int):
    """Função unificada para excluir laje"""

    def recarregar_tela():
        """Helper para recarregar a tela de detalhes"""
        from src.infrastructure.database.repositories import RepositorioCliente, RepositorioProjeto

        # Busca dados atualizados
        repo_projeto = RepositorioProjeto()
        projeto_atualizado = repo_projeto.get_by_id(projeto_id)

        if projeto_atualizado:
            repo_cliente = RepositorioCliente()
            cliente = repo_cliente.get_by_id(projeto_atualizado.cliente_id)

            # Limpa e preserva elementos importantes
            page.controls.clear()
            appbar = page.appbar
            navigation_bar = page.navigation_bar

            # Recarrega tela
            from src.core.projeto.detalhes_projeto import tela_detalhes_projeto

            tela_detalhes_projeto(page, projeto_atualizado, cliente)

            # Restaura elementos
            if appbar:
                page.appbar = appbar
            if navigation_bar:
                page.navigation_bar = navigation_bar

            page.update()

    def confirmar_exclusao(e):
        dlg_confirmacao.open = False
        page.update()

        try:
            # Executa exclusão
            with postgres.session_scope() as session:
                servico = ServicoLaje(RepositorioLaje(session))
                sucesso, mensagem = servico.excluir_laje(laje_id, projeto_id)

                if sucesso:
                    # Mostra mensagem e recarrega
                    page.snack_bar = ft.SnackBar(content=ft.Text(mensagem), bgcolor=ft.colors.GREEN)
                    page.snack_bar.open = True
                    page.update()

                    # Recarrega a tela
                    recarregar_tela()
                else:
                    # Mostra erro
                    page.snack_bar = ft.SnackBar(content=ft.Text(mensagem), bgcolor=ft.colors.ERROR)
                    page.snack_bar.open = True
                    page.update()

        except Exception as error:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao excluir: {error}"), bgcolor=ft.colors.ERROR)
            page.snack_bar.open = True
            page.update()

    # Cria diálogo de confirmação
    dlg_confirmacao = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Exclusão"),
        content=ft.Text("Deseja realmente excluir esta laje?\nEsta ação não poderá ser desfeita!"),
        actions=[
            ft.TextButton("Não", on_click=lambda e: setattr(dlg_confirmacao, "open", False)),
            ft.ElevatedButton("Sim", on_click=confirmar_exclusao, style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.RED)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Exibe diálogo
    page.dialog = dlg_confirmacao
    dlg_confirmacao.open = True
    page.update()
