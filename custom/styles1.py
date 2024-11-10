from dataclasses import dataclass
import flet as ft
from typing import Dict, Any, Callable


@dataclass
class CoresPrincipais:
    """Define as cores principais do tema"""

    PRIMARIA = ft.colors.BLUE
    SECUNDARIA = ft.colors.PURPLE
    AVISO = ft.colors.RED
    FUNDO = ft.colors.BLACK
    SUPERFICIE = ft.colors.GREY_900
    TEXTO = ft.colors.WHITE


class GerenciadorTema:
    """Gerenciador de tema da aplicação"""

    def __init__(self, pagina: ft.Page):
        self.pagina = pagina
        self.gerenciador_estilos = GerenciadorEstilos()

    def aplicar_tema(self):
        """Aplica o tema à página"""
        self._configurar_janela()
        self._configurar_layout()
        self._configurar_tema()
        self._configurar_fundo()

    def _configurar_janela(self):
        """Configura as propriedades da janela"""
        configuracao_janela = {
            "width": 400,
            "height": 700,
            "title_bar_hidden": False,
            "frameless": False,
            "opacity": 1.0,
        }

        for prop, valor in configuracao_janela.items():
            setattr(self.pagina.window, prop, valor)

        self.pagina.window.center()

    def _configurar_layout(self):
        """Configura o layout da página"""
        self.pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.pagina.padding = 20
        self.pagina.spacing = 20

    def _configurar_tema(self):
        """Configura o tema da aplicação"""
        self.pagina.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=self.gerenciador_estilos.cores.PRIMARIA,
                secondary=self.gerenciador_estilos.cores.SECUNDARIA,
            ),
            font_family="Arial",
        )

    def _configurar_fundo(self):
        """Configura o fundo da página"""
        self.pagina.bgcolor = ft.colors.with_opacity(
            0.1, self.gerenciador_estilos.cores.FUNDO
        )
        self.pagina.gradient = ft.LinearGradient(
            colors=[
                self.gerenciador_estilos.cores.FUNDO,
                self.gerenciador_estilos.cores.SUPERFICIE,
            ],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
        )


class GerenciadorEstilos:
    """Gerenciador de estilos da aplicação"""

    def __init__(self):
        self.cores = CoresPrincipais()

    @property
    def estilo_input(self) -> Dict[str, Any]:
        """Estilo padrão para campos de entrada"""
        return {
            "keyboard_type": ft.KeyboardType.NUMBER,
            "width": 300,
            "bgcolor": ft.colors.with_opacity(0.8, self.cores.SUPERFICIE),
            "border_radius": 10,
            "text_size": 16,
            "border": ft.InputBorder.UNDERLINE,
            "color": self.cores.TEXTO,
        }

    @property
    def estilo_botao_base(self) -> ft.ButtonStyle:
        """Estilo base para botões"""
        return ft.ButtonStyle(animation_duration=500)

    def criar_estilo_hover(self, cor: str) -> ft.ButtonStyle:
        """Cria um estilo de hover personalizado"""
        return ft.ButtonStyle(
            animation_duration=500,
            color=self.cores.TEXTO,
            overlay_color=ft.colors.with_opacity(0.2, cor),
            side={
                ft.ControlState.DEFAULT: ft.BorderSide(1, cor),
                ft.ControlState.HOVERED: ft.BorderSide(2, cor),
            },
        )

    @property
    def estilo_container(self) -> Dict[str, Any]:
        """Estilo padrão para containers"""
        return {
            "bgcolor": ft.colors.with_opacity(0.9, self.cores.SUPERFICIE),
            "margin": 15,
            "padding": 20,
            "alignment": ft.alignment.center,
            "width": 350,
            "border_radius": 15,
            "shadow": ft.BoxShadow(
                spread_radius=2,
                blur_radius=20,
                color=ft.colors.with_opacity(0.2, self.cores.TEXTO),
                offset=ft.Offset(0, 4),
                blur_style=ft.ShadowBlurStyle.NORMAL,
            ),
        }


class GerenciadorEfeitoHover:
    """Gerenciador de efeitos hover"""

    def __init__(self):
        self.gerenciador_estilos = GerenciadorEstilos()

    def criar_handler_hover(self, cor: str):
        """Cria um handler para efeito hover"""
        def handler_hover(e):
            e.control.style = self.gerenciador_estilos.criar_estilo_hover(cor) if e.data == "true" else self.gerenciador_estilos.estilo_botao_base
            e.control.update()

        return handler_hover

    @property
    def hover_padrao(self):
        return self.criar_handler_hover(self.gerenciador_estilos.cores.PRIMARIA)

    @property
    def hover_aviso(self):
        return self.criar_handler_hover(self.gerenciador_estilos.cores.AVISO)

    @property
    def hover_secundario(self):
        return self.criar_handler_hover(self.gerenciador_estilos.cores.SECUNDARIA)


class ControleBotao:
    """Classe para controle de botões"""

    @staticmethod
    def gerenciar_hover_botao(e, cor):
        """Gerencia o efeito hover nos botões"""
        if e.data == "true":  # Mouse entrou
            e.control.scale = 1.00
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
def aplicar_tema(pagina: ft.Page):
    """Aplica o tema à página"""
    gerenciador_tema = GerenciadorTema(pagina)
    gerenciador_tema.aplicar_tema()


def obter_efeitos_hover_botao():
    """Retorna os efeitos hover"""
    gerenciador_hover = GerenciadorEfeitoHover()
    return {
        "padrao": gerenciador_hover.hover_padrao,
        "aviso": gerenciador_hover.hover_aviso,
        "secundario": gerenciador_hover.hover_secundario,
    }


def obter_estilos():
    """Retorna os estilos padrão"""
    gerenciador_estilos = GerenciadorEstilos()
    return {
        "input": gerenciador_estilos.estilo_input,
        "container": gerenciador_estilos.estilo_container,
        "botao_base": gerenciador_estilos.estilo_botao_base,
    }


def obter_efeito_container(e, cor):
    '''Efeito de hover para container'''

    return ControleBotao.gerenciar_hover_botao(e, cor)