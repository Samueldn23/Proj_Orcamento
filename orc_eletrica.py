import flet as ft

def mostrar_eletrica(page):
    page.controls.clear()
    page.add(ft.Text("Tela de elétrica", size=24))

    altura_input = ft.TextField(label="Altura (m)", keyboard_type=ft.KeyboardType.NUMBER)
    largura_input = ft.TextField(label="Largura (m)", keyboard_type=ft.KeyboardType.NUMBER)
    valor_m2_input = ft.TextField(label="Valor por m²", keyboard_type=ft.KeyboardType.NUMBER)

    resultado_text = ft.Text("Custo Total: R$0.00", size=18)

    def calcular(e):
        try:
            altura = float(altura_input.value)
            largura = float(largura_input.value)
            valor_m2 = float(valor_m2_input.value)
            custo_total = altura * largura * valor_m2
            resultado_text.value = f"Custo Total: R${custo_total:.2f}"
            page.update()
        except ValueError:
            resultado_text.value = "Por favor, insira valores válidos."
            page.update()

    calcular_button = ft.ElevatedButton(text="Calcular", on_click=calcular, width=200)
    voltar_button = ft.ElevatedButton(text="Voltar", 
                                       on_click=lambda e: voltar(page), 
                                       width=200, bgcolor=ft.colors.RED, color=ft.colors.WHITE)

    page.add(altura_input, largura_input, valor_m2_input, calcular_button, resultado_text, voltar_button)
    page.update()

def voltar(page):
    page.controls.clear()
    from mn_orcamento import orcamento  # Importa a função orcamento
    orcamento(page)  # Retorna à tela de Orçamento