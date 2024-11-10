import flet as ft
import custom.styles as stl
import custom.button as btn
import locale
import asyncio
import random


# Define a localidade para pt_BR
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


class ExemploPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.animation_running = True
        self.setup_page()
        self.create_components()
        self.setup_layout()
        self.start_animation()

    def setup_page(self) -> None:
        """Configura as propriedades iniciais da página"""
        self.page.controls.clear()
        self.page.padding = 20
        self.page.spacing = 20
        self.page.window.center()

    def create_components(self) -> None:
        """Cria todos os componentes da página"""
        self.create_title()
        self.create_image()
        self.create_container()
        self.create_buttons()

    def create_title(self) -> None:
        """Cria o título da página"""
        self.title = ft.Text(
            "Tela de Exemplo",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE,
            text_align=ft.TextAlign.CENTER,
        )

    def create_image(self) -> None:
        """Cria e configura o componente de imagem"""
        self.img = ft.Image(
            src="assets/img/iconFundacao.ico",
            height=150,
            width=150,
            fit=ft.ImageFit.CONTAIN,
            offset=ft.Offset(y=0, x=0),
            scale=ft.Scale(scale=1),
            opacity=1,
            animate_offset=self._create_animation(),
            animate_scale=self._create_animation(),
            animate_opacity=self._create_animation(),
        )

    def _create_animation(self) -> ft.Animation:
        """Cria uma animação padrão"""
        return ft.Animation(duration=2000, curve=ft.AnimationCurve.EASE_IN_OUT)

    def create_container(self) -> None:
        """Cria e configura o container principal"""
        self.container = ft.Container(
            content=ft.Column(
                [self.img],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLACK,
            border_radius=10,
            width=300,
            height=300,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.colors.WHITE,
            ),
        )
        self.container.on_hover = self._on_container_hover

    def create_buttons(self) -> None:
        """Cria os botões da interface"""
        self.voltar_btn = ft.ElevatedButton(
            text="Voltar",
            on_click=lambda e: btn.voltar.principal(self.page),
            width=100,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )
        self.voltar_btn.on_hover = stl.hover_effect_voltar

        self.toggle_btn = ft.ElevatedButton(
            text="Pausar Animação",
            on_click=self._toggle_animation,
            width=150,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )

    def setup_layout(self) -> None:
        """Organiza os componentes na página"""
        self.page.add(
            ft.Column(
                [
                    self.title,
                    self.container,
                    ft.Row(
                        [self.voltar_btn, self.toggle_btn],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            )
        )

    def _on_container_hover(self, e: ft.HoverEvent) -> None:
        """Gerencia o efeito hover do container"""
        self.container.bgcolor = (
            ft.colors.GREY_900 if e.data == "true" else ft.colors.BLACK
        )
        self.container.scale = 1.05 if e.data == "true" else 1.0
        self.container.update()

    def _toggle_animation(self, e) -> None:
        """Alterna o estado da animação"""
        self.animation_running = not self.animation_running
        self.toggle_btn.text = (
            "Continuar Animação" if not self.animation_running else "Pausar Animação"
        )
        self.toggle_btn.update()

    async def animate_image(self) -> None:
        """Executa a animação da imagem"""
        while True:
            if self.animation_running:
                self.img.offset = ft.Offset(
                    random.uniform(-0.8, 0.8), random.uniform(-0.8, 0.8)
                )
                self.img.scale = ft.Scale(scale=random.uniform(0.5, 1.5))
                self.img.opacity = random.uniform(0.3, 1.0)
                self.page.update()
            await asyncio.sleep(1)

    def start_animation(self) -> None:
        """Inicia a tarefa de animação"""
        self.page.run_task(self.animate_image)
        self.page.update()


def exemplo(page: ft.Page) -> None:
    ExemploPage(page)
