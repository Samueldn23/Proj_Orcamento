from dataclasses import dataclass
import flet as ft
from typing import Dict, Any, Callable


@dataclass
class ThemeColors:
    """Define as cores principais do tema"""

    PRIMARY = ft.colors.BLUE
    SECONDARY = ft.colors.PURPLE
    WARNING = ft.colors.RED
    BACKGROUND = ft.colors.BLACK
    SURFACE = ft.colors.GREY_900
    TEXT = ft.colors.WHITE


class ThemeManager:
    """Gerenciador de tema da aplicação"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.style_manager = StyleManager()

    def apply_theme(self):
        """Aplica o tema à página"""
        self._configure_window()
        self._configure_layout()
        self._configure_theme()
        self._configure_background()

    def _configure_window(self):
        """Configura as propriedades da janela"""
        window_config = {
            "width": 400,
            "height": 700,
            "title_bar_hidden": False,
            "frameless": False,
            "opacity": 1.0,
        }

        for prop, value in window_config.items():
            setattr(self.page.window, prop, value)

        self.page.window.center()

    def _configure_layout(self):
        """Configura o layout da página"""
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.padding = 20
        self.page.spacing = 20

    def _configure_theme(self):
        """Configura o tema da aplicação"""
        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=self.style_manager.colors.PRIMARY,
                secondary=self.style_manager.colors.SECONDARY,
            ),
            font_family="Arial",
        )

    def _configure_background(self):
        """Configura o fundo da página"""
        self.page.bgcolor = ft.colors.with_opacity(
            0.1, self.style_manager.colors.BACKGROUND
        )
        self.page.gradient = ft.LinearGradient(
            colors=[
                self.style_manager.colors.BACKGROUND,
                self.style_manager.colors.SURFACE,
            ],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
        )


class StyleManager:
    """Gerenciador de estilos da aplicação"""

    def __init__(self):
        self.colors = ThemeColors()

    @property
    def input_style(self) -> Dict[str, Any]:
        """Estilo padrão para campos de entrada"""
        return {
            "keyboard_type": ft.KeyboardType.NUMBER,
            "width": 300,
            "bgcolor": ft.colors.with_opacity(0.8, self.colors.SURFACE),
            "border_radius": 10,
            "text_size": 16,
            # "text_align": ft.TextAlign.CENTER,
            "border": ft.InputBorder.UNDERLINE,
            "color": self.colors.TEXT,
        }

    @property
    def button_base_style(self) -> ft.ButtonStyle:
        """Estilo base para botões"""
        return ft.ButtonStyle(
            animation_duration=500,
            # shape=ft.RoundedRectangleBorder(radius=10),
            # padding=20,
        )

    def create_hover_style(self, color: str) -> ft.ButtonStyle:
        """Cria um estilo de hover personalizado"""
        return ft.ButtonStyle(
            animation_duration=500,
            color=self.colors.TEXT,
            # bgcolor=color,
            # shape=ft.RoundedRectangleBorder(radius=10),
            overlay_color=ft.colors.with_opacity(0.2, color),
            side={
                ft.ControlState.DEFAULT: ft.BorderSide(1, color),
                ft.ControlState.HOVERED: ft.BorderSide(2, color),
            },
        )

    @property
    def container_style(self) -> Dict[str, Any]:
        """Estilo padrão para containers"""
        return {
            "bgcolor": ft.colors.with_opacity(0.9, self.colors.SURFACE),
            "margin": 15,
            "padding": 20,
            "alignment": ft.alignment.center,
            "width": 350,
            "border_radius": 15,
            "shadow": ft.BoxShadow(
                spread_radius=2,
                blur_radius=20,
                color=ft.colors.with_opacity(0.2, self.colors.TEXT),
                offset=ft.Offset(0, 4),
                blur_style=ft.ShadowBlurStyle.NORMAL,
            ),
        }


class HoverEffectManager:
    """Gerenciador de efeitos hover"""

    def __init__(self):
        self.style_manager = StyleManager()

    def create_hover_handler(self, color: str):
        """Cria um handler para efeito hover"""

        def hover_handler(e):
            if e.data == "true":
                e.control.style = self.style_manager.create_hover_style(color)
            else:
                e.control.style = self.style_manager.button_base_style
            e.control.update()

        return hover_handler

    @property
    def default_hover(self):
        return self.create_hover_handler(self.style_manager.colors.PRIMARY)

    @property
    def warning_hover(self):
        return self.create_hover_handler(self.style_manager.colors.WARNING)

    @property
    def secondary_hover(self):
        return self.create_hover_handler(self.style_manager.colors.SECONDARY)


class BtnController:
    """Classe para controle de botões"""

    @staticmethod
    def handle_button_hover(e, cor):
        """Gerencia o efeito hover nos botões"""
        if e.data == "true":  # Mouse entrou
            e.control.scale = 1.05
            e.control.shadow = ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=cor,
                offset=ft.Offset(0, 0),
            )
            e.control.border_radius = 25
            e.control.padding = 2
        else:  # Mouse saiu
            e.control.scale = 1.0
            e.control.shadow = None
        e.control.update()


# Funções de utilidade para uso externo
def apply_theme(page: ft.Page):
    """Aplica o tema à página"""
    theme_manager = ThemeManager(page)
    theme_manager.apply_theme()


def get_btn_hover_effects():
    """Retorna os efeitos hover"""
    hover_manager = HoverEffectManager()
    return {
        "default": hover_manager.default_hover,
        "warning": hover_manager.warning_hover,
        "secondary": hover_manager.secondary_hover,
    }


def get_styles():
    """Retorna os estilos padrão"""
    style_manager = StyleManager()
    return {
        "input": style_manager.input_style,
        "container": style_manager.container_style,
        "button_base": style_manager.button_base_style,
    }


def get_btn_container(e, cor):
    """Retorna o container padrão para botões"""
    return BtnController.handle_button_hover(e, cor)