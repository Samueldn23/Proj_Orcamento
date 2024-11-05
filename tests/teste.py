import flet as ft
import custom.styles as stl
import custom.button as btn


def pageteste(page: ft.Page):
    # Definir os temas e estilos da aplicação
    page.controls.clear()
    page.title = "Aplicativo de Orçamento para Construção"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.BLUE,
            secondary=ft.colors.ORANGE,
            error=ft.colors.RED,
        )
    )

    # Criar os widgets da interface
    project_name = ft.TextField(
        label="Nome do Projeto", hint_text="Digite o nome do projeto"
    )
    project_type = ft.Dropdown(
        label="Tipo de Projeto",
        options=[
            ft.dropdown.Option("Construção Nova"),
            ft.dropdown.Option("Reforma"),
            ft.dropdown.Option("Ampliação"),
        ],
    )
    project_area = ft.TextField(
        label="Área do Projeto (m²)", hint_text="Digite a área do projeto"
    )
    materials_cost = ft.TextField(
        label="Custo dos Materiais", hint_text="Digite o custo dos materiais"
    )
    labor_cost = ft.TextField(
        label="Custo da Mão de Obra", hint_text="Digite o custo da mão de obra"
    )
    total_cost = ft.TextField(label="Custo Total", read_only=True)
    calculate_button = ft.ElevatedButton("Calcular Orçamento")

    def calculate_total_cost(event):
        try:
            area = float(project_area.value)
            materials = float(materials_cost.value)
            labor = float(labor_cost.value)
            total = area * (materials + labor)
            total_cost.value = f"R$ {total:.2f}"
        except ValueError:
            total_cost.value = "Valores inválidos"
        page.update()

    calculate_button.on_click = calculate_total_cost

    voltar_btn = ft.ElevatedButton(
        text="Voltar",
        on_click=lambda e: btn.voltar.principal(page),
        on_hover=stl.hover_effect_voltar,
    )

    # Organizar os widgets na página
    page.add(
        ft.Column(
            [
                project_name,
                project_type,
                project_area,
                materials_cost,
                labor_cost,
                total_cost,
                calculate_button,
                voltar_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=16,
        )
    )


# ft.app(target=main)
