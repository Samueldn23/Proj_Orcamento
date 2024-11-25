"""Arquivo para armazenar os estilos e botões customizados. styles_utils.py"""

from dataclasses import dataclass
from typing import Any, Callable, Dict

import flet as ft


@dataclass
class ThemeColors:
    """Define as cores do tema da aplicação"""

    PRIMARY = ft.colors.BLUE
    SECONDARY = ft.colors.WHITE
    VOLTAR = ft.colors.RED
    SOMBRA_CTR = ft.colors.GREY_900
    CONTAINER = ft.colors.BLACK87
    TEXTO = ft.colors.WHITE
    IMPUT = ft.colors.GREY_900


class StyleManager:
    """Gerenciador central de estilos e efeitos"""

    def __init__(self, page: ft.Page = None):
        self.page = page
        self.colors = ThemeColors()

    def apply_theme(self, page=None):
        """Aplica o tema à página"""
        self.page = page or self.page
        if not self.page:
            raise ValueError("Page não foi definida")

        # Configuração da janela
        window_config = {
            "width": 450,
            "height": 750,
            "title_bar_hidden": False,
            "frameless": False,
            "opacity": 1.0,
        }
        for prop, value in window_config.items():
            setattr(self.page.window, prop, value)
        self.page.window.center()

        # Configuração do layout
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.padding = 20
        self.page.spacing = 20

        # Configuração do tema
        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=self.colors.PRIMARY,
                secondary=self.colors.SECONDARY,
            ),
            font_family="Arial",
        )

        # Configuração do fundo
        self.page.bgcolor = ft.colors.with_opacity(0.1, self.colors.SOMBRA_CTR)
        self.page.gradient = ft.LinearGradient(
            colors=[self.colors.SOMBRA_CTR, self.colors.CONTAINER],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
        )

    @staticmethod
    def create_button_hover_effect(
        button: ft.Control, text_color: str, hover_color: str
    ) -> Callable:
        """Cria efeito hover para botões"""

        def on_hover(e):
            if e.data == "true":
                button.style = ft.ButtonStyle(
                    animation_duration=500,
                    color=text_color,
                    icon_color=ThemeColors.TEXTO,
                    overlay_color=ft.colors.with_opacity(0.2, hover_color),
                    side={
                        ft.ControlState.DEFAULT: ft.BorderSide(1, hover_color),
                        ft.ControlState.HOVERED: ft.BorderSide(2, hover_color),
                    },
                )
            else:
                button.style = ft.ButtonStyle(bgcolor=None, shadow_color=None)
            button.update()

        return on_hover

    @staticmethod
    def create_container_hover_effect(hover_color: str) -> Callable:
        """Cria efeito hover para containers"""

        def on_hover(e):
            if e.data == "true":
                e.control.scale = 1.05
                e.control.shadow = ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=hover_color,
                    offset=ft.Offset(0, 0),
                )
            else:
                e.control.scale = 1.0
                e.control.shadow = None
            e.control.update()

        return on_hover

    def create_button(
        self,
        text: str,
        on_click: Callable,
        icon: str = None,
        width: int = 200,
        icon_color: str = ThemeColors.PRIMARY,
        hover_icon_color: str = ThemeColors.SECONDARY,
        text_color: str = ThemeColors.SECONDARY,
        hover_color: str = ThemeColors.PRIMARY,  # Permite None explicitamente
        hover_color_button: str = None,  # Agora é opcional
        # shape: str = ft.RoundedRectangleBorder(radius=0),
    ) -> ft.Container:
        """Cria um botão customizado com container"""

        # Define o hover_color_button com base em hover_color
        if hover_color_button is None:
            hover_color_button = (
                hover_color if hover_color is not None else ThemeColors.PRIMARY
            )

        # Cria o ícone somente se o ícone for definido
        icone = ft.Icon(name=icon, color=icon_color) if icon else None

        # Cria os conteúdos do botão (com ou sem ícone)
        button_contents = [
            icone if icone else ft.Container(),  # Adiciona o ícone ou um espaço vazio
            ft.Text(text, size=15),
        ]

        # Cria o botão
        button = ft.ElevatedButton(
            content=ft.Row(
                button_contents,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            on_click=on_click,
            width=width,
        )

        # Define a função de hover personalizada para o botão e o ícone
        def button_hover_effect(e):
            if icone:  # Só manipula o ícone se ele existir
                if e.data == "true":
                    # Quando o mouse entra no botão
                    icone.color = hover_icon_color  # Muda a cor do ícone
                else:
                    # Quando o mouse sai do botão
                    icone.color = icon_color  # Restaura a cor original do ícone
                icone.update()

        # Adiciona o efeito hover para o botão e o ícone
        button.on_hover = lambda e: (
            self.create_button_hover_effect(button, text_color, hover_color_button)(e),
            button_hover_effect(e),
        )

        # Cria o container para o botão
        container = ft.Container(
            content=ft.Column(
                controls=[button],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=2,
            border_radius=25,
            animate=ft.animation.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
            on_hover=self.create_container_hover_effect(hover_color),
        )

        return container

    def create_button_custom(
        self,
        text: str,
        on_click: Callable,
        icon: str,
        width: int = 200,
        icon_color: str = ThemeColors.PRIMARY,
        hover_icon_color: str = ThemeColors.SECONDARY,  # Cor do ícone no hover
        text_color: str = ThemeColors.SECONDARY,
        hover_color: str = ThemeColors.PRIMARY,
    ) -> ft.Container:
        """Cria um botão customizado com container"""
        # Cria a imagem inicialmente com animação de cor
        image = ft.Image(
            src=icon,
            width=22,
            height=22,
            color=icon_color,  # Cor original da imagem5
        )

        # Cria o botão
        button = ft.ElevatedButton(
            content=ft.Row(
                [image, ft.Text(text, size=15)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            on_click=on_click,
            width=width,
        )

        # Define a função de hover personalizada para o botão e o ícone
        def button_hover_effect(e):
            if e.data == "true":
                # Quando o mouse entra no botão
                image.color = hover_icon_color  # Muda a cor do ícone
            else:
                # Quando o mouse sai do botão
                image.color = icon_color  # Restaura a cor original do ícone
            image.update()

        # Adiciona o efeito hover ao botão
        button.on_hover = self.create_button_hover_effect(
            button=button,
            text_color=text_color,
            hover_color=hover_color,
        )

        # Adiciona o efeito hover para o ícone
        button.on_hover = lambda e: (
            self.create_button_hover_effect(button, text_color, hover_color)(e),
            button_hover_effect(e),
        )

        # Cria o container para o botão
        container = ft.Container(
            content=ft.Column(
                controls=[button],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=2,
            border_radius=25,
            animate=ft.animation.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
            on_hover=self.create_container_hover_effect(hover_color),
        )

        return container

    @property
    def input_style(self) -> Dict[str, Any]:
        """Estilo padrão aprimorado para inputs"""
        return {
            "width": 350,  # Largura ligeiramente maior para destacar o campo
            "bgcolor": ft.colors.with_opacity(
                0.9, self.colors.IMPUT
            ),  # Fundo mais suave
            "border_radius": 12,  # Cantos mais arredondados para suavidade
            "text_size": 16,  # Tamanho de texto agradável para leitura
            "border": ft.InputBorder.OUTLINE,  # Borda inferior apenas
            "border_color": ft.colors.with_opacity(
                0.5, self.colors.PRIMARY
            ),  # Cor da borda ao redor
            "focused_border_color": self.colors.SECONDARY,  # Realce da borda ao focar
            "content_padding": 12,  # Espaçamento interno para uma aparência mais espaçosa
            "color": self.colors.TEXTO,  # Cor do texto padrão
        }

    @property
    def button_style(self) -> Dict[str, Any]:
        """Estilo padrão para botões"""
        return {
            "width": 200,
            "color": self.colors.TEXTO,
            "bgcolor": self.colors.PRIMARY,
        }

    @property
    def container_style(self) -> Dict[str, Any]:
        """Estilo padrão aprimorado para containers"""
        return {
            "bgcolor": ft.colors.with_opacity(
                0.20, self.colors.CONTAINER
            ),  # Fundo com leve transparência
            "margin": 20,  # Margem maior para melhor separação visual
            "padding": 25,  # Espaçamento interno mais confortável
            "alignment": ft.alignment.center,  # Centralização consistente
            "width": 400,  # Largura mais expressiva para destacar o container
            "border_radius": 20,  # Cantos mais arredondados para um visual elegante
            "border": ft.Border(
                bottom=ft.BorderSide(
                    1, ft.colors.with_opacity(0.3, self.colors.VOLTAR)
                ),  # Borda leve e discreta
                # right=ft.BorderSide(1, ft.colors.with_opacity(0.3, self.colors.VOLTAR)),
            ),
            "shadow": ft.BoxShadow(
                spread_radius=3,  # Ampliação sutil do alcance da sombra
                blur_radius=15,  # Redução do desfoque para uma sombra mais limpa
                color=ft.colors.with_opacity(
                    0.25, self.colors.TEXTO
                ),  # Sombra com cor mais evidente
                offset=ft.Offset(
                    0, 5
                ),  # Deslocamento da sombra para um efeito de elevação
                blur_style=ft.ShadowBlurStyle.OUTER,  # Sombra externa mais suave
            ),
            "animate": ft.animation.Animation(
                400, ft.AnimationCurve.EASE_IN_OUT
            ),  # Animação suave para alterações
            "on_hover": self.create_container_hover_effect(
                self.colors.SOMBRA_CTR
            ),  # Efeito de hover personalizado
        }


# Funções de utilidade para uso externo
def get_style_manager(page: ft.Page = None) -> StyleManager:
    """Retorna uma instância do gerenciador de estilos"""
    return StyleManager(page)