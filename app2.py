import flet as ft
from menu import mostrar_menu


def main (page: ft.Page):
    mostrar_menu(page)


if __name__ == "__main__":
    ft.app(target=main)