import flet as ft
import custom.styles as stl
import custom.button as btn
from typing import Optional
import locale

#Configuração da localização
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

class Fundacao:

    def __init__(self, page: ft.Page):
        self.page = page
        self.resultado_text: Optional[ft.Text] = None
        self._init_controls()

    def _init_controls(self):
        """Inicializa os controles da página"""
        self.espessura_input = ft.TextField(
            label="Espessura (cm)",
            prefix_icon=ft.icons.SPACE_BAR_ROUNDED,
            suffix_text="centimetros",
            # keyboard_type=ft.KeyboardType.NUMBER,
            **stl.input_style,
        )
        self.altura_input = ft.TextField(
            label="Altura (m)",
            prefix_icon=ft.icons.HEIGHT,
            suffix_text="metros",
            # keyboard_type=ft.KeyboardType.NUMBER,
            **stl.input_style,
        )
        self.comprimento_input = ft.TextField(
            label="Comprimento (m)",
            prefix_icon=ft.icons.STRAIGHTEN,
            suffix_text="metros",
            # keyboard_type=ft.KeyboardType.NUMBER,
            **stl.input_style,
        )

        self.valor_m3_input = ft.TextField(
            label="Valor por m³",
            prefix_icon=ft.icons.ATTACH_MONEY,
            suffix_text="R$",
            # keyboard_type=ft.KeyboardType.NUMBER,
            **stl.input_style,
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
            return False, "Por favor, insira apenas números válidos!"

    def _calcular_orcamento(self) -> tuple[float,float]:
        """calcula a area e os custo total"""
        altura = float(self.altura_input.value)
        espessura = float (self.espessura_input.value)
        comprimento = float(self.comprimento_input.value)
        valor_m3 = float(self.valor_m3_input.value)

        area = altura * comprimento * espessura
        custo_total = area * valor_m3

        return area, custo_total
    
    def _update_resultado(self, area: float, custo_total: float):
        """Atualiza o texto de resultado"""
        self.area_text.value = f"Área total: {area:.2f} m²"
        self.resultado_text.value = (
            f"Custo Total: {locale.currency(custo_total, grouping=True)}"
        )
        self.page.update()

    def calcular(self, _):
        """manipula o evento de calculo"""
        valid, message = self._validate_inputs()
        if not valid:   
            self.resultado_text.value = message
            self.area_text.valeu = ""
            self.page.update()
            return
        
        try:
            area, custo_total = self._calcular_orcamento()
            self._update_resultado(area, custo_total)
        except Exception as e:
            self.resultado_text.value = f"Erro ao calcular: {str(e)}"
            self.area_text.value = ""
            self.page.update()


    def build(self):
        """Constrói a interface da página"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Cálculo de Fundação",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE,
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                self.altura_input,
                                self.comprimento_input,
                                self.espessura_input,
                                self.valor_m3_input,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        **stl.container_style,
                    ),
                    ft.ElevatedButton(
                        text="Calcular",
                        icon=ft.icons.CALCULATE,
                        on_click=self.calcular,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        **stl.button_style,
                    ),
                    self.area_text,
                    self.resultado_text,
                    ft.ElevatedButton(
                        text="Voltar",
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: btn.voltar.orcamento(self.page),
                        on_hover=stl.hover_effect_voltar,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=0,
            alignment=ft.alignment.center,
        )


def mostrar_fundacao(page: ft.Page):
    """função helper para mostar a página de calculo de fundação"""

    page.controls.clear()
    fundacao_calculator = Fundacao(page)
    page.add(fundacao_calculator.build())
    page.update()