import App.login
from App.models import criar_tabelas
import flet as ft
import App
import styles as stl

# Variável global para controlar a criação das tabelas
tabelas_criadas = False

def main(page):
    global tabelas_criadas
    
    print("Inicializando a aplicação...")  # Mensagem de depuração
    
    if not tabelas_criadas:  # Verifica se as tabelas já foram criadas
        print("Criando as tabelas...")
        criar_tabelas()  # Garante que as tabelas sejam criadas uma única vez
        tabelas_criadas = True  # Define como True para não repetir a criação

    # Exemplo de interface mínima do Flet
    stl.aplicar_tema(page)
    page.title = "App de Orçamento"
    App.login.mostrar_login(page)
    page.add(ft.Text("Bem-vindo ao sistema de orçamento!"))
    
    page.update()
    print("Aplicação iniciada com sucesso!")
# Inicializa a aplicação Flet
if __name__ == "__main__":
    try:
        ft.app(target=main)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
