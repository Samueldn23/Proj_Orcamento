import flet as ft
import custom.styles as stl
import custom.button as btn
import locale
import asyncio
import random

# Define a localidade para pt_BR
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


def exemplo(page: ft.Page):
    page.controls.clear()

    # Título da tela
    page.add(
        ft.Text(
            "Tela de Exemplo", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE
        )
    )

    # Configuração da imagem com animação
    img = ft.Image(
        src="assets/img/pngwing.com (1).png",
        height=150,
        width=150,
        fit=ft.ImageFit.CONTAIN,
        offset=ft.Offset(y=0, x=0),
        scale=ft.Scale(scale=1),
        opacity=1,
        animate_offset=ft.Animation(duration=2000, curve=ft.AnimationCurve.EASE_IN_OUT),
        animate_scale=ft.Animation(duration=2000, curve=ft.AnimationCurve.EASE_IN_OUT),
        animate_opacity=ft.Animation(
            duration=2000, curve=ft.AnimationCurve.EASE_IN_OUT
        ),
    )

    # Configuração do container
    container = ft.Container(
        content=ft.Column([img], alignment=ft.MainAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.BLACK,
        border_radius=10,
        width=300,
        height=300,
    )

    # Função para animações da imagem
    async def animate_image():
        while True:
            img.offset = ft.Offset(random.uniform(-1, 1), random.uniform(-1, 1))
            img.scale = ft.Scale(scale=random.uniform(0.5, 1.5))
            img.opacity = random.uniform(0.3, 1.0)
            page.update()  # Atualiza a página de forma assíncrona
            await asyncio.sleep(1)

    # Eventos de sombra ao passar o mouse sobre o container
    def on_mouse_enter(e):
        if e.data == "true":  # Mouse sobre o botão
            container.bgcolor = ft.colors.GREY_900
            container.update()
        else:  # Mouse saiu do botão
            container.bgcolor = ft.colors.BLACK
            container.update()

    # Adiciona eventos ao container
    container.on_hover = on_mouse_enter

    # Botão Voltar com efeito de hover
    voltar_btn = ft.ElevatedButton(
        text="Voltar",
        on_click=lambda e: btn.voltar.principal(page),
        width=100,
    )
    voltar_btn.on_hover = stl.hover_effect_voltar

    # Adiciona os elementos à página
    page.add(container, voltar_btn)

    # Inicia a tarefa de animação assíncrona
    page.run_task(animate_image)
    page.update()
