import flet as ft
import locale

# Define a localidade para pt_BR
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  

def mostrar_contrapiso(page):
    page.controls.clear()
    page.add(ft.Text("Contrapiso", size=24))

    comprimento_input = ft.TextField(label="Comprimento (m)", keyboard_type=ft.KeyboardType.NUMBER)
    largura_input = ft.TextField(label="Largura (m)", keyboard_type=ft.KeyboardType.NUMBER)
    valor_input = ft.TextField(label="Valor do m² (R$)", keyboard_type=ft.KeyboardType.NUMBER)
    resultado_text = ft.Text("Custo Total: R$ 0.00", size=18)

    def calcular(e):
        try:
            comprimento = float(comprimento_input.value)
            largura = float(largura_input.value)
            ValorM2 = float(valor_input.value)
            calculo_m2 = largura * comprimento
            custo_total = calculo_m2 * ValorM2
            resultado_text.value = f"Custo Total cm: {locale.currency(custo_total, grouping=True)}"
            page.update()

        except ValueError:
            resultado_text.value = "Por favor, insira valores válidos."
            page.update()
            
    calcular_button = ft.ElevatedButton(text="Calcular", on_click=calcular, width=200)
    voltar_button = ft.ElevatedButton(text="Voltar", 
                                        on_click=lambda e: voltar(page), 
                                        width=200, bgcolor=ft.colors.RED, color=ft.colors.WHITE)

    page.add(comprimento_input, largura_input, valor_input, calcular_button, resultado_text, voltar_button)
    page.update()

def voltar(page):
    page.controls.clear()
    from mn_orcamento import orcamento  # Importa a função orcamento
    orcamento(page)  # Retorna à tela de Orçamento