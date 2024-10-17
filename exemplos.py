import flet as ft
import styles as stl
import locale
import asyncio

# Define a localidade para pt_BR
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def exemplo(page: ft.Page):
    page.controls.clear()
    
    # Título da tela
    page.add(ft.Text("Tela de Exemplo", size=24))

    # Função assíncrona para animações
    async def animate_image():
        while True:
            # Animação de entrada
            img.offset.y = 0
            img.scale.scale = 1
            img.opacity = 1
            img.update()
            await asyncio.sleep(3)  # Tempo de espera antes da próxima animação

            # Animação de saída
            img.offset.y = 0.2  # Move para baixo
            img.scale.scale = 0.5  # Reduz o tamanho
            img.opacity = 0.5  # Torna semi-transparente
            img.update()
            await asyncio.sleep(3)

    # Configuração da imagem
    img = ft.Image(
        src="static\\img\\pngwing.com (1).png",
        height=150,
        width=150,
        fit=ft.ImageFit.CONTAIN,
        offset=ft.Offset(y=0, x=0),
        scale=ft.Scale(scale=1),
        opacity=1,
        animate_offset=ft.Animation(duration=3000, curve=ft.AnimationCurve.EASE),
        animate_scale=ft.Animation(duration=3000, curve=ft.AnimationCurve.EASE),
        animate_opacity=ft.Animation(duration=3000, curve=ft.AnimationCurve.EASE),
    )
    
    # Configuração do container sem rotação
    container = ft.Container(
        content=ft.Column(
            [
                img
            ],
            spacing=50
        ),
        bgcolor=ft.colors.TRANSPARENT,
        border_radius=10,
    )

    # Função para mover o container em direção ao mouse
    def on_mouse_move(e):
        mouse_x, mouse_y = e.data['mouseX'], e.data['mouseY']
        container.offset.x = mouse_x - (container.width / 2)  # Centraliza o container no mouse
        container.offset.y = mouse_y - (container.height / 2)  # Centraliza o container no mouse
        container.update()

    # Adiciona evento de movimento do mouse ao container
    container.on_mouse_move = on_mouse_move

    # Função para aplicar sombra ao passar o mouse
    def on_mouse_enter(e):
        container.shadows = [ft.BoxShadow(color=ft.colors.BLUE, blur_radius=30, spread_radius=10)]
        container.update()

    def on_mouse_leave(e):
        container.shadows = []
        container.update()

    # Adiciona eventos de entrada e saída do mouse ao container
    container.on_mouse_enter = on_mouse_enter
    container.on_mouse_leave = on_mouse_leave

    # Botão Voltar com animação de hover
    voltar_btn = ft.ElevatedButton(
        text="Voltar", 
        on_click=lambda e: voltar(page), 
        **stl.button_style_voltar
    )

    # Animação de hover no botão
    voltar_btn.on_hover = lambda e: setattr(voltar_btn, "bgcolor", ft.colors.RED if e.data == "enter" else ft.colors.WHITE)
    container.on_hover = lambda e: setattr(voltar_btn, "bgcolor", ft.colors.RED if e.data == "enter" else ft.colors.WHITE)

    # Adiciona os elementos à página
    page.add(container, voltar_btn)
    
    # Inicia a tarefa de animação
    page.run_task(animate_image)
    page.update()

def voltar(page):
    page.controls.clear()    
    from mn_orcamento import orcamento  # Importa a função orcamento
    orcamento(page)  # Retorna à tela de Orçamento

# Exemplo de execução
# ft.app(target=exemplo)