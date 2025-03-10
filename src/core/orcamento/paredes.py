"""Módulo para cálculo de orçamento de paredes"""

import locale

import flet as ft

from src.core.projeto.detalhes_projeto import atualizar_custo_estimado
from src.custom.styles_utils import get_style_manager
from src.data.tijolos import carregar_tijolos, salvar_tijolos
from src.infrastructure.database.connections import Session
from src.infrastructure.database.models.construction import Wall
from src.navigation.router import navegar_orcamento

# Configurações
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
gsm = get_style_manager()
TIPOS_TIJOLOS = carregar_tijolos()
session = Session()


class ParedeCalculator:
    """Classe para cálculo de orçamento de paredes"""

    def __init__(self, page: ft.Page, cliente, projeto):
        self.page = page
        self.cliente = cliente
        self.projeto = projeto
        self.resultado_text: ft.Text | None = None
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

        self.tipo_tijolo_dropdown = ft.Dropdown(
            label="Tipo de Tijolo",
            leading_icon=ft.Icons.GRID_VIEW,
            options=[ft.dropdown.Option(key=tipo) for tipo in TIPOS_TIJOLOS.keys()],
            value=next(iter(TIPOS_TIJOLOS.keys())),  # Seleciona o primeiro por padrão
            expand=True,  # Adicione esta linha
            **gsm.input_style,
        )

        self.edit_preco_button = ft.IconButton(
            icon=ft.Icons.EDIT,
            tooltip="Editar preço do tijolo",
            on_click=self._abrir_dialog_preco,
        )

        self.qtd_tijolos_text = ft.Text(
            size=16,
            text_align=ft.TextAlign.CENTER,
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

    def _calcular_orcamento(self) -> tuple[float, float, int]:
        """Calcula a área, o custo total e a quantidade de tijolos"""
        altura = float(self.altura_input.value)
        comprimento = float(self.comprimento_input.value)
        valor_m2 = float(self.valor_m2_input.value)

        area = altura * comprimento
        mao_obra = area * valor_m2

        # Cálculo da quantidade de tijolos
        tijolo_selecionado = TIPOS_TIJOLOS[self.tipo_tijolo_dropdown.value]
        area_tijolo = tijolo_selecionado["largura"] * tijolo_selecionado["altura"]
        tijolos_por_m2 = 1 / area_tijolo
        quantidade_tijolos = int(area * tijolos_por_m2)

        return area, mao_obra, quantidade_tijolos

    def _update_resultado(self, area: float, mao_obra: float, qtd_tijolos: int):
        """Atualiza o texto de resultado"""
        tijolo_selecionado = TIPOS_TIJOLOS[self.tipo_tijolo_dropdown.value]
        preco_unitario = tijolo_selecionado["preco_unitario"]
        custo_tijolos = qtd_tijolos * preco_unitario
        custo_total = mao_obra + custo_tijolos

        self.area_text.value = f"Área total: {area:.2f} m²"
        self.qtd_tijolos_text.value = (
            f"Quantidade de tijolos: {qtd_tijolos} unidades\n"
            f"Custo estimado dos tijolos: "
            f"{locale.currency(custo_tijolos, grouping=True)}\n"
            f"Custo mão de obra: {locale.currency(mao_obra, grouping=True)}"
        )
        self.resultado_text.value = f"Custo Total estimado: {locale.currency(custo_total, grouping=True)}"
        self.page.update()

    def calcular(self, _):
        """Manipula o evento de cálculo"""
        valid, message = self._validate_inputs()
        if not valid:
            self.page.open(ft.SnackBar(content=ft.Text(message), bgcolor=ft.Colors.ERROR))
            self.resultado_text.value = ""
            self.area_text.value = ""
            self.qtd_tijolos_text.value = ""
            self.page.update()
            return

        try:
            area, mao_obra, quantidade_tijolos = self._calcular_orcamento()
            self._update_resultado(area, mao_obra, quantidade_tijolos)

            # Força atualização da UI
            self.page.update()

        except ValueError as e:
            self.page.open(
                ft.SnackBar(
                    content=ft.Text(f"Erro ao calcular: {e!s}"),
                    bgcolor=ft.Colors.ERROR,
                )
            )
            self.page.update()

    def salvar(self, e):
        try:
            # Validar e calcular
            valid, message = self._validate_inputs()
            if not valid:
                self.page.open(ft.SnackBar(content=ft.Text(message), bgcolor=ft.Colors.ERROR))
                return

            area, mao_obra, quantidade_tijolos = self._calcular_orcamento()
            tijolo_selecionado = TIPOS_TIJOLOS[self.tipo_tijolo_dropdown.value]
            custo_tijolos = quantidade_tijolos * tijolo_selecionado["preco_unitario"]
            custo_total = mao_obra + custo_tijolos

            # Criar nova parede no banco
            nova_parede = Wall(
                projeto_id=self.projeto.id,  # Corrigido de orcamento_id para projeto_id
                altura=float(self.altura_input.value),
                comprimento=float(self.comprimento_input.value),
                area=area,
                valor_m2=float(self.valor_m2_input.value),
                tipo_tijolo=self.tipo_tijolo_dropdown.value,
                quantidade_tijolos=quantidade_tijolos,
                custo_tijolos=custo_tijolos,
                custo_mao_obra=mao_obra,
                custo_total=custo_total,
            )

            session.add(nova_parede)
            session.commit()

            # Atualizar o custo estimado do projeto
            atualizar_custo_estimado(self.projeto.id)

            # Mostrar mensagem de sucesso
            self.page.open(
                ft.SnackBar(
                    content=ft.Text("Parede salva com sucesso!"),
                    bgcolor=ft.Colors.GREEN,
                )
            )

            # Navegar para detalhes do projeto
            navegar_orcamento(self.page, self.cliente, self.projeto)

        except Exception as error:
            self.page.open(ft.SnackBar(content=ft.Text(f"Erro ao salvar: {error!s}"), bgcolor=ft.Colors.ERROR))

    def _abrir_dialog_preco(self, e):
        tijolo_selecionado = self.tipo_tijolo_dropdown.value
        dlg_preco = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Preço"),
            content=ft.TextField(
                label="Novo preço",
                value=str(TIPOS_TIJOLOS[tijolo_selecionado]["preco_unitario"]),
                keyboard_type=ft.KeyboardType.NUMBER,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(dlg_preco)),
                ft.TextButton("Confirmar", on_click=lambda e: self._confirmar_preco(e, dlg_preco)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.open(dlg_preco)

    def _confirmar_preco(self, e, dlg):
        try:
            novo_preco = float(dlg.content.value)
            tijolo_selecionado = self.tipo_tijolo_dropdown.value
            TIPOS_TIJOLOS[tijolo_selecionado]["preco_unitario"] = novo_preco
            salvar_tijolos(TIPOS_TIJOLOS)  # Salva as alterações no arquivo
            self.page.close(dlg)

            # Recalcula os valores se houver dados nos campos
            if self.altura_input.value and self.comprimento_input.value and self.valor_m2_input.value:
                self.calcular(None)

        except ValueError:
            self.page.open(ft.SnackBar(content=ft.Text("Por favor, insira um valor válido")))

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
                                    "Cálculo de Parede",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE,
                                ),
                                ft.Row(
                                    [
                                        ft.Text(
                                            f"Projeto: {self.projeto.nome}",
                                            size=12,
                                            # weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.BLUE_300,
                                        ),
                                        ft.Text(
                                            f"Cliente: {self.cliente['nome']}",
                                            size=12,
                                            # weight=ft.FontWeight.BOLD,
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
                                            content=self.altura_input,
                                            expand=1,
                                        ),
                                        ft.Container(
                                            content=self.comprimento_input,
                                            expand=1,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                ft.Row(
                                    [
                                        ft.Container(
                                            content=self.tipo_tijolo_dropdown,
                                            expand=3,
                                        ),
                                        ft.Container(
                                            content=self.valor_m2_input,
                                            expand=2,
                                        ),
                                    ],
                                    spacing=5,
                                ),
                                self.edit_preco_button,
                            ],
                            spacing=10,
                        ),
                        padding=10,
                        # bgcolor=ft.Colors.ON_SURFACE_VARIANT,
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
                                self.area_text,
                                self.qtd_tijolos_text,
                                self.resultado_text,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                            spacing=5,
                        ),
                        # bgcolor=ft.Colors.ON_SURFACE_VARIANT,
                        padding=10,
                        border_radius=10,
                        # visible=bool(self.resultado_text.value),
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


def mostrar_parede(page: ft.Page, cliente, projeto):
    """Função helper para mostrar a página de cálculo de parede"""
    page.controls.clear()
    parede_calculator = ParedeCalculator(page, cliente, projeto)
    page.add(parede_calculator.build())
    page.update()
