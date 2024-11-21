import flet as ft

def TelaCadastroCliente(page: ft.Page):
    page.title = "Cadastro de Clientes"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    name_field = ft.TextField(label="Nome", width=300)
    phone_field = ft.TextField(label="Telefone", width=300)
    email_field = ft.TextField(label="E-mail", width=300)



    view = ft.View(
        "/clients",
        controls=[
            ft.AppBar(
                title=ft.Text("Cadastro de Clientes"),
                leading=ft.Icon(ft.icons.PERSON_ADD),
                bgcolor=ft.colors.BLUE,
                actions=[ft.IconButton(ft.icons.HOME, on_click=lambda _: page.go("/dashboard"))],
            ),
            ft.Column(
                controls=[
                    name_field,
                    phone_field,
                    email_field,
                    ft.ElevatedButton("Salvar", on_click=save_client),
                    ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/dashboard")),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
    )

    page.add(view)
    page.update()

    def save_client(e):
        print("Salvando cliente...")