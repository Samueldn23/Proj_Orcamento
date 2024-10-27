import flet as ft
import styles as stl
from utils import voltar

def mostrar_eletrica(page):
    page.controls.clear()
    page.add(ft.Text("Tela de elétrica", size=24))

    ponto_input = ft.TextField(label="pontos elétricos", **stl.input_style)

    valorPonto_input = ft.TextField(label= "Valor cobrado por ponto", **stl.input_style)

    resultado_text = ft.Text("Custo Total: R$ 0.00", size=18)

    def calcular(e):
        try:
            ponto = float(ponto_input.value)

            valor_ponto = float(valorPonto_input.value)
            custo_total = ponto *   valor_ponto
            resultado_text.value = f"Custo Total: R$ {custo_total:.2f}"
            page.update()
        except ValueError:
            resultado_text.value = "Por favor, insira valores válidos."
            page.update()

    calcular_button = ft.ElevatedButton(text="Calcular", on_click=calcular, **stl.button_style)
    voltar_button = ft.ElevatedButton(text="Voltar", on_click=lambda e: voltar.orcamento(page), **stl.button_style_voltar)

    page.add(ponto_input, valorPonto_input, calcular_button, resultado_text, voltar_button)
    page.update()
