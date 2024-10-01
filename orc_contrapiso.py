import flet as ft
import locale

# Define a localidade para pt_BR
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def mostrar_contrapiso(page):
    page.controls.clear()

    page.add(ft.Text("Contrapiso", size=24))

    comprimento_input = ft.TextField(label="Comprimento (m)", keyboard_type=ft.KeyboardType.NUMBER)
    largura_input = ft.TextField(label="Largura (m)", keyboard_type=ft.KeyboardType.NUMBER)
    valor_input = ft.TextField(label="Valor do Metro (R$)", keyboard_type=ft.KeyboardType.NUMBER)
    espessura_input = ft.TextField(label="Espessura (Cm)", keyboard_type=ft.KeyboardType.NUMBER, visible=False)
    resultado_text = ft.Text("Custo Total: R$ 0.00", size=18)

    # Função para calcular o custo
    def calcular(e):
        try:
            comprimento = float(comprimento_input.value)
            largura = float(largura_input.value)
            ValorM2 = float(valor_input.value)

            if switch.value:  # switch para metros cúbicos
                espessura = float(espessura_input.value)
                calculo_m3 = largura * comprimento * (espessura / 100)  # Converter espessura para metros
                custo_total = calculo_m3 * ValorM2
            else:  # metros quadrados
                calculo_m2 = largura * comprimento
                custo_total = calculo_m2 * ValorM2

            resultado_text.value = f"Custo Total: {locale.currency(custo_total, grouping=True)}"
        except ValueError:
            resultado_text.value = "Por favor, insira valores válidos."
        page.update()

    # Função para atualizar visibilidade do campo de espessura
    def atualizar(e):
        espessura_input.visible = switch.value
        page.update()

    switch = ft.Switch(label="Metro Quadrado para Metro Cúbico", on_change=atualizar, value=False)

    calcular_button = ft.ElevatedButton(text="Calcular", on_click=calcular, width=200)
    voltar_button = ft.ElevatedButton(text="Voltar", on_click=lambda e: voltar(page), width=200, bgcolor=ft.colors.RED, color=ft.colors.WHITE)

    page.add(comprimento_input, largura_input, valor_input, espessura_input, switch, calcular_button, resultado_text, voltar_button)
    page.update()

def voltar(page):
    page.controls.clear()
    from mn_orcamento import orcamento  # Importa a função orcamento
    orcamento(page)  # Retorna à tela de Orçamento
