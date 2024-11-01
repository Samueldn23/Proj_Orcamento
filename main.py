import flet as ft

import custom.styles as stl
import user.login
from models.db import criar_tabelas

# Variável global para controlar a criação das tabelas
tabelas_criadas = False


def main(page):
    global tabelas_criadas
    # Garante que as tabelas sejam criadas uma única vez
    if not tabelas_criadas:
        criar_tabelas()
        tabelas_criadas = True

    # Exemplo de interface mínima do Flet
    stl.aplicar_tema(page)
    page.title = "App de Orçamento"
    page.add(ft.Text("Bem-vindo ao sistema de orçamento!"))
    user.login.mostrar_login(page)  # Chamada direta para a tela de login

    page.update()


# Inicializa a aplicação Flet
if __name__ == "__main__":
    try:
        ft.app(target=main)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
