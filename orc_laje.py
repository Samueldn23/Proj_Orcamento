import flet as ft

def mostrar_laje(page):

    page.controls.clear()

    page.add(ft.Text("orçamento da laje", size=24))
    comprimento_input = ft.TextField(label="Comprimento (m)", keyboard_type=ft.KeyboardType.NUMBER)
    largura_input = ft.TextField(label="Largura (m)", keyboard_type=ft.KeyboardType.NUMBER)
    altura_input = ft.TextField(label="Espessura (cm)", keyboard_type=ft.KeyboardType.NUMBER)
    valor_m3_input = ft.TextField(label="Valor por m³", keyboard_type=ft.KeyboardType.NUMBER)


    resultado_text = ft.Text("Custo Total: R$ 0.00", size=18)


    def calcular(e):

        try:
            comprimento = float(comprimento_input.value)
            largura = float(largura_input.value)
            espessura = float(altura_input.value)

            volor_m3 = float(valor_m3_input.value)
            custo_total = comprimento * largura * (espessura / 100) * volor_m3
            resultado_text.value = f"Custo Total: R$ {custo_total:.2f}"
            page.update()

        except ValueError:

            resultado_text.value = "Por favor, insira valores válidos."
            page.update()

    switch =  ft.Switch(
            #adaptive=True,
            label="Adaptive Switch",
            value=True,
        )

    c1 = ft.Switch(label="Unchecked switch", value=False)

    calcular_button = ft.ElevatedButton(text="Calcular", on_click=calcular, width=200)
    voltar_button = ft.ElevatedButton(text="Voltar", 
                                        on_click=lambda e: voltar(page), 
                                        width=200, bgcolor=ft.colors.RED, color=ft.colors.WHITE)

    page.add(comprimento_input, largura_input,altura_input, valor_m3_input, switch,c1, calcular_button, resultado_text, voltar_button)
    page.update()

def voltar(page):
    
    page.controls.clear()
    from mn_orcamento import orcamento  # Importa a função orcamento
    orcamento(page)  # Retorna à tela de Orçamento 