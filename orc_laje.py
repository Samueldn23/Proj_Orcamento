import flet as ft

def mostrar_laje(page):

    page.controls.clear()

    page.add(ft.Text("orçamento da laje", size=24))
    comprimento_input = ft.TextField(label="Comprimento (m)", keyboard_type=ft.KeyboardType.NUMBER)
    largura_input = ft.TextField(label="Largura (m)", keyboard_type=ft.KeyboardType.NUMBER)
    altura_input = ft.TextField(label="Espessura (cm)", keyboard_type=ft.KeyboardType.NUMBER)
    valor_m3_input = ft.TextField(label="Valor por (m³)", keyboard_type=ft.KeyboardType.NUMBER)


    resultado_text = ft.Text("Custo Total: R$ 0.00", size=18)

    switch =  ft.Switch(
            label="cm para mm",
            on_change=lambda e: atualizar(page),
            value=False,
        
        )

    def atualizar(e):
        if switch.value ==False:
            altura_input.label="Espessura (cm)"
        else:
            altura_input.label="Espessura (mm)"
        
            
        page.update()

        

    def calcular(e):

        try:
            comprimento = float(comprimento_input.value)
            largura = float(largura_input.value)
            espessura = float(altura_input.value)
            volor_m3 = float(valor_m3_input.value)

            if switch.value == False:
                espessura = espessura/100
            

            custo_total = comprimento * largura * espessura  * volor_m3
            resultado_text.value = f"Custo Total: R$ {custo_total:.2f}"
            page.update()

        except ValueError:

            resultado_text.value = "Por favor, insira valores válidos."
            page.update()

    

    calcular_button = ft.ElevatedButton(text="Calcular", on_click=calcular, width=200)
    voltar_button = ft.ElevatedButton(text="Voltar", 
                                        on_click=lambda e: voltar(page), 
                                        width=200, bgcolor=ft.colors.RED, color=ft.colors.WHITE)

    page.add(comprimento_input, largura_input,altura_input, valor_m3_input, switch, calcular_button, resultado_text, voltar_button)
    page.update()

def voltar(page):
    
    page.controls.clear()
    from mn_orcamento import orcamento  # Importa a função orcamento
    orcamento(page)  # Retorna à tela de Orçamento 