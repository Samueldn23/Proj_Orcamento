import locale

import flet as ft

# Configuração da localização para formatação de moeda
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


class Construcao:
    """Classe base para diferentes tipos de construção"""

    def __init__(self, tipo, area, custo_total):
        self.tipo = tipo
        self.area = area
        self.custo_total = custo_total

    def criar_card(self):
        """Método para criar um card com informações da construção"""
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        # Ícone com cor baseada no tipo de construção
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.HOUSE_SIDING if self.tipo == "Parede" else ft.Icons.ELECTRIC_BOLT,
                                color=ft.Colors.WHITE,
                                size=18,
                            ),
                            width=32,
                            height=32,
                            border_radius=ft.border_radius.all(16),
                            bgcolor=ft.Colors.BLUE_600 if self.tipo == "Parede" else ft.Colors.ORANGE_600,
                            alignment=ft.alignment.center,
                        ),
                        ft.VerticalDivider(width=10, opacity=0),  # Espaçamento invisível
                        # Informações principais
                        ft.Column(
                            [
                                ft.Text(
                                    f"{self.tipo}",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"Área: {self.area}m²",
                                    size=12,
                                    weight=ft.FontWeight.W_500,
                                    color=ft.Colors.GREY_700,
                                ),
                                ft.Text(
                                    locale.currency(float(self.custo_total), grouping=True),
                                    size=13,
                                    color=ft.Colors.GREEN_700,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            spacing=3,
                            expand=True,
                        ),
                        # Botões de ação
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT_SQUARE,
                                        tooltip="Editar",
                                        icon_color=ft.Colors.BLUE_600,
                                        icon_size=20,
                                        on_click=lambda e: print("editar_construcao(construcao)"),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_FOREVER,
                                        tooltip="Excluir",
                                        icon_color=ft.Colors.RED_600,
                                        icon_size=20,
                                        on_click=lambda e: print("excluir_construcao(construcao)"),
                                    ),
                                ],
                                spacing=1,
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.padding.all(12),
                bgcolor=ft.Colors.GREY_900,
            ),
            elevation=2,
            surface_tint_color=ft.Colors.BLUE_100,
        )


class Parede(Construcao):
    def __init__(self, area, custo_total, tipo_tijolo, quantidade_tijolos):
        super().__init__("Parede", area, custo_total)
        self.tipo_tijolo = tipo_tijolo
        self.quantidade_tijolos = quantidade_tijolos

    def criar_card(self):
        card = super().criar_card()

        # Adiciona informações específicas sobre a parede em um container separado
        info_container = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.GRID_4X4, size=14, color=ft.Colors.BLUE_GREY_600),
                                ft.Text(
                                    f"Tipo: {self.tipo_tijolo}",
                                    size=11,
                                    color=ft.Colors.BLUE_GREY_600,
                                ),
                            ],
                            spacing=4,
                        ),
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.APPS, size=14, color=ft.Colors.BLUE_GREY_600),
                                ft.Text(
                                    f"Qtd: {self.quantidade_tijolos} tijolos",
                                    size=11,
                                    color=ft.Colors.BLUE_GREY_600,
                                ),
                            ],
                            spacing=4,
                        ),
                        margin=ft.margin.only(left=10),
                    ),
                ],
            ),
            margin=ft.margin.only(top=5, left=42),  # Alinha com o texto principal
        )

        # Acessa a coluna principal e adiciona o container de informações
        coluna_principal = card.content.content.controls[2]
        coluna_principal.controls.append(info_container)

        # Ajusta o espaçamento da coluna
        coluna_principal.spacing = 5

        return card


class Eletrica(Construcao):
    def __init__(self, area, custo_total, tipo_fio, quantidade_fios):
        super().__init__("Elétrica", area, custo_total)
        self.tipo_fio = tipo_fio
        self.quantidade_fios = quantidade_fios

    def criar_card(self):
        card = super().criar_card()
        card.content.content.controls[1].controls.append(
            ft.Text(
                f"{self.quantidade_fios} fios ({self.tipo_fio})",
                size=11,
                color=ft.Colors.BLUE_GREY_400,
            )
        )
        return card


class Telhado(Construcao):
    def __init__(self, area, custo_total, tipo_telhas, quantidade_telhas):
        super().__init__("Telhado", area, custo_total)
        self.tipo_telhas = tipo_telhas
        self.quantidade_telhas = quantidade_telhas

    def criar_card(self):
        card = super().criar_card()
        card.content.content.controls[1].controls.append(
            ft.Text(
                f"{self.quantidade_telhas} telhas ({self.tipo_telhas})",
                size=11,
                color=ft.Colors.BLUE_GREY_400,
            )
        )
        return card


def criar_card_parede(construcao):
    """Cria um card para exibir informações da construção"""
    return ft.Card(
        content=ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.HOUSE_SIDING, color=ft.Colors.BLUE, size=20),
                    # ft.VerticalDivider(width=10),
                    ft.Column(
                        [
                            ft.Text(
                                f"Área: {construcao.area}m² - {construcao.tipo_tijolo}",
                                size=12,
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Row(
                                [
                                    ft.Text(
                                        f"{construcao.quantidade_tijolos} tijolos",
                                        size=11,
                                        color=ft.Colors.BLUE_GREY_400,
                                    ),
                                    ft.Text(
                                        locale.currency(float(construcao.custo_total), grouping=True),
                                        size=11,
                                        color=ft.Colors.GREEN,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        tooltip="Editar",
                                        on_click=lambda e: print("editar_construcao(construcao)"),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        tooltip="Excluir",
                                        on_click=lambda e: print("excluir_construcao(construcao)"),
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                        spacing=3,
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.all(8),
        ),
        elevation=1,
    )


# Esqueleto para criação de cards para outros tipos de construções
def criar_card_outro_tipo(construcao):
    """Cria um card para exibir informações de outro tipo de construção"""
    # Implementação futura
    pass
