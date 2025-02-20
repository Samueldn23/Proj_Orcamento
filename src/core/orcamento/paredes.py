"""Módulo para cálculo de orçamento de paredes. base/orcamentos/parede.py"""

import locale
from typing import Optional

import flet as ft

from src.navigation.router import navegar_orcamento
from src.custom.styles_utils import get_style_manager

# Adicione após as importações existentes

TIPOS_TIJOLOS = {
    "Tijolo 8 Furos (9x19x19)": {
        "nome": "Tijolo 8 Furos",
        "largura": 0.19,
        "altura": 0.19,
        "profundidade": 0.09,
        "preco_unitario": 1.20  # Preço exemplo
    },
    "Tijolo 6 Furos (9x14x24)": {
        "nome": "Tijolo 6 Furos",
        "largura": 0.24,
        "altura": 0.14,
        "profundidade": 0.09,
        "preco_unitario": 0.90
    },
    "Bloco Cerâmico (14x19x29)": {
        "nome": "Bloco Cerâmico",
        "largura": 0.29,
        "altura": 0.19,
        "profundidade": 0.14,
        "preco_unitario": 1.50
    }
}

# Configuração da localização
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
gsm = get_style_manager()


class ParedeCalculator:
    """Classe para cálculo de orçamento de paredes"""

    def __init__(self, page: ft.Page, cliente, projeto):
        self.page = page
        self.cliente = cliente
        self.projeto = projeto
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

        self.tipo_tijolo_dropdown = ft.Dropdown(
            label="Tipo de Tijolo",
            prefix_icon=ft.Icons.GRID_VIEW,
            options=[
                ft.dropdown.Option(key=tipo) for tipo in TIPOS_TIJOLOS.keys()
            ],
            value=list(TIPOS_TIJOLOS.keys())[0],  # Seleciona o primeiro por padrão
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
        custo_total = area * valor_m2

        # Cálculo da quantidade de tijolos
        tijolo_selecionado = TIPOS_TIJOLOS[self.tipo_tijolo_dropdown.value]
        area_tijolo = tijolo_selecionado["largura"] * tijolo_selecionado["altura"]
        tijolos_por_m2 = 1 / area_tijolo
        quantidade_tijolos = int(area * tijolos_por_m2)
        
        return area, custo_total, quantidade_tijolos

    def _update_resultado(self, area: float, custo_total: float, qtd_tijolos: int):
        """Atualiza o texto de resultado"""
        tijolo_selecionado = TIPOS_TIJOLOS[self.tipo_tijolo_dropdown.value]
        self.area_text.value = f"Área total: {area:.2f} m²"
        self.qtd_tijolos_text.value = (
            f"Quantidade de tijolos necessários: {qtd_tijolos} unidades\n"
            f"Custo estimado dos tijolos: "
            f"{locale.currency(qtd_tijolos * tijolo_selecionado['preco_unitario'], grouping=True)}"
        )
        self.resultado_text.value = (
            f"Custo Total (mão de obra): {locale.currency(custo_total, grouping=True)}"
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
            area, custo_total, quantidade_tijolos = self._calcular_orcamento()
            self._update_resultado(area, custo_total, quantidade_tijolos)
        except ValueError as e:
            self.resultado_text.value = f"Erro ao calcular: {str(e)}"
            self.area_text.value = ""
            self.page.update()

    def salvar(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("teste"), bgcolor=ft.Colors.GREEN)
        )

    def _abrir_dialog_preco(self, e):
        """Abre um diálogo para editar o preço do tijolo"""
        tijolo_selecionado = TIPOS_TIJOLOS[self.tipo_tijolo_dropdown.value]
        
        preco_input = ft.TextField(
            label="Novo preço unitário",
            value=str(tijolo_selecionado["preco_unitario"]),
            prefix_icon=ft.Icons.ATTACH_MONEY,
            keyboard_type=ft.KeyboardType.NUMBER,
            **gsm.input_style
        )

        def salvar_preco(e):
            try:
                novo_preco = float(preco_input.value)
                if novo_preco <= 0:
                    raise ValueError("Preço deve ser maior que zero")
                    
                TIPOS_TIJOLOS[self.tipo_tijolo_dropdown.value]["preco_unitario"] = novo_preco
                dlg.open = False
                self.page.update()
                
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text("Preço atualizado com sucesso!"),
                        bgcolor=ft.colors.GREEN
                    )
                )
            except ValueError:
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text("Por favor, insira um valor válido!"),
                        bgcolor=ft.colors.RED
                    )
                )

        dlg = ft.AlertDialog(
            title=ft.Text(f"Editar preço - {tijolo_selecionado['nome']}"),
            content=preco_input,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg, 'open', False)),
                ft.TextButton("Salvar", on_click=salvar_preco),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def build(self):
        """Constrói a interface da página"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        f"Cálculo de Parede para {self.cliente['nome']}",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE,
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                self.altura_input,
                                self.comprimento_input,
                                ft.Row(
                                    controls=[
                                        self.tipo_tijolo_dropdown,
                                        self.edit_preco_button,
                                    ],
                                    spacing=0,
                                ),
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
                    self.qtd_tijolos_text,  # Adicione esta linha
                    self.resultado_text,
                    ft.Row(
                        [
                            gsm.create_button(
                                text="Salvar",
                                on_click=self.salvar,
                                icon=ft.Icons.SAVE,
                                hover_color=ft.Colors.GREEN,
                                width=130,
                            ),
                            gsm.create_button(
                                text="Voltar",
                                on_click=lambda _: navegar_orcamento(
                                    self.page, self.cliente, self.projeto
                                ),
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
                spacing=20,
            ),
            padding=0,
            alignment=ft.alignment.center,
        )


def mostrar_parede(page: ft.Page, cliente, projeto):
    """Função helper para mostrar a página de cálculo de parede"""
    page.controls.clear()
    parede_calculator = ParedeCalculator(page, cliente, projeto)
    page.add(parede_calculator.build())
    page.update()
