import flet as ft
import styles as stl
import locale

# Define a localidade para pt_BR
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def mostrar_parede(page):
    page.controls.clear()
    page.add(ft.Text("Tela de Parede", size=24))

    altura_input = ft.TextField(label="Altura (m)", **stl.input_style)
    comprimento_input = ft.TextField(label="comprimento (m)", **stl.input_style)
    valor_m2_input = ft.TextField(label="Valor por m²", **stl.input_style)

    resultado_text = ft.Text("Custo Total: R$ 0.00", size=18)

    def calcular(e):
        try:
            altura = float(altura_input.value)
            comprimento = float(comprimento_input.value)
            valor_m2 = float(valor_m2_input.value)

            custo_total = altura * comprimento * valor_m2

            resultado_text.value = f"Custo Total: {locale.currency(custo_total, grouping=True)}"
            page.update()
        except ValueError:
            resultado_text.value = "Por favor, insira valores válidos."
            page.update()

    calcular_btn = ft.ElevatedButton(text="Calcular", on_click=calcular, **stl.button_style)
    voltar_btn = ft.ElevatedButton(text="Voltar", on_click=lambda e: voltar(page),**stl.button_style_voltar)

    page.add(
        ft.Container(            
                    content=ft.Column(
                        [
                            altura_input, comprimento_input, valor_m2_input
                        ],
                        alignment="center",
                        spacing=10  # Espaçamento entre os botões
                    ),
                    **stl.container_style
                ),
    )

    page.add(calcular_btn, resultado_text, voltar_btn)
    page.update()

def voltar(page):
    page.controls.clear()    
    from mn_orcamento import orcamento  # Importa a função orcamento
    orcamento(page)  # Retorna à tela de Orçamento