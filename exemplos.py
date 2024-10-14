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
        scale=ft.Scale(scale=1),  # Começa com escala normal
        opacity=1,
        animate_offset=ft.Animation(duration=3000, curve=ft.AnimationCurve.EASE),
        animate_scale=ft.Animation(duration=3000, curve=ft.AnimationCurve.EASE),
        animate_opacity=ft.Animation(duration=3000, curve=ft.AnimationCurve.EASE),
    )

    # Botão Voltar com animação de hover
    voltar_btn = ft.ElevatedButton(
        text="Voltar", 
        on_click=lambda e: voltar(page), 
        **stl.button_style_voltar
    )

    # Animação de hover no botão
    voltar_btn.on_hover = lambda e: setattr(voltar_btn, "bgcolor", ft.colors.RED if e.data == "enter" else ft.colors.WHITE)

    # Adiciona os elementos à página
    page.add(img, voltar_btn)
    
    # Inicia a tarefa de animação
    page.run_task(animate_image)
    page.update()

def voltar(page):
    page.controls.clear()    
    from mn_orcamento import orcamento  # Importa a função orcamento
    orcamento(page)  # Retorna à tela de Orçamento

# Exemplo de execução
# ft.app(target=exemplo)