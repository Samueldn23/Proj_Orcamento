import App.user.login
from App.models import criar_tabelas, cadastrar_usuario
import flet as ft
import App
import styles as stl

# Variável global para controlar a criação das tabelas
tabelas_criadas = False

def main(page):
    global tabelas_criadas

    print("Inicializando a aplicação...")  # Mensagem de depuração
    
    # Garante que as tabelas sejam criadas uma única vez
    if not tabelas_criadas:
        print("Criando as tabelas se necessário...")
        criar_tabelas()
        tabelas_criadas = True

    # Exemplo de interface mínima do Flet
    stl.aplicar_tema(page)
    page.title = "App de Orçamento"
    page.add(ft.Text("Bem-vindo ao sistema de orçamento!"))
    App.user.login.mostrar_login(page)  # Chamada direta para a tela de login

    
    page.update()
    print("Aplicação iniciada com sucesso!")

# Inicializa a aplicação Flet
if __name__ == "__main__":
    try:
        ft.app(target=main)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")