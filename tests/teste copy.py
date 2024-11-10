import flet as ft

def main(page: ft.page):
    page.title = "orçamento da laje"
    lista_nome = ["kaio", "samuel"]
    page.add(
        
        ft.Image(
            src= "assets/img/iconFundacao.png",
            width=22,
            height=22,            
        ),
        ft.Divider(),

        



        ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Image(
                        src= "assets/img/iconFundacao.png",
                        width=22,
                        height=22,            
                    ),
                    
                    ft.Text('Fundação',size=15)
                ]
            ),
            on_click=lambda _: print(lista_nome[1]),
            width=150
        ),
    )
    
    

if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="assets",
    )

