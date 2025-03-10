"""Módulo com funções para edição de lajes existentes."""

from decimal import Decimal

import flet as ft

from src.core.orcamento.laje.tipos_laje import TipoLaje, carregar_tipos_laje
from src.core.projeto.detalhes_projeto import atualizar_custo_estimado, carregar_detalhes_projeto
from src.infrastructure.database.connections.postgres import postgres
from src.infrastructure.database.models.construcoes import Lajes

# Carrega os tipos de laje
TIPOS_LAJE = carregar_tipos_laje()


def editar_laje(page, laje_id, projeto_id):
    """Abre um diálogo para edição de laje existente"""
    # Busca dados da laje existente
    with postgres.session_scope() as session:
        laje = session.query(Lajes).filter_by(id=laje_id).first()
        if not laje:
            page.snack_bar = ft.SnackBar(content=ft.Text("Laje não encontrada."), bgcolor=ft.colors.RED_700)
            page.snack_bar.open = True
            page.update()
            return

        comprimento = float(laje.comprimento)
        largura = float(laje.largura)
        espessura = float(laje.espessura)
        valor_m3 = float(laje.valor_m3)
        tipo_laje = getattr(laje, "tipo_laje", TipoLaje.MACICA.name)

    # Controles para o formulário de edição
    titulo = ft.Text("Editar Laje", size=20, weight=ft.FontWeight.BOLD)

    comprimento_field = ft.TextField(
        label="Comprimento (m)",
        value=str(comprimento),
        width=200,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    largura_field = ft.TextField(
        label="Largura (m)",
        value=str(largura),
        width=200,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    espessura_field = ft.TextField(
        label="Espessura (cm)",
        value=str(espessura),
        width=200,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    valor_m3_field = ft.TextField(
        label="Valor por m³ (R$)",
        value=str(valor_m3),
        width=200,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    tipo_laje_dropdown = ft.Dropdown(
        label="Tipo de Laje",
        width=200,
        options=[
            ft.dropdown.Option(key=TipoLaje.MACICA.name, text="Laje Maciça"),
            ft.dropdown.Option(key=TipoLaje.NERVURADA.name, text="Laje Nervurada"),
            ft.dropdown.Option(key=TipoLaje.PRE_MOLDADA.name, text="Laje Pré-Moldada"),
        ],
        value=tipo_laje,
    )

    # Função para salvar as alterações
    def salvar_alteracoes(e):
        try:
            # Validação dos dados
            novo_comprimento = float(comprimento_field.value)
            nova_largura = float(largura_field.value)
            nova_espessura = float(espessura_field.value)
            novo_valor_m3 = float(valor_m3_field.value)
            novo_tipo_laje = tipo_laje_dropdown.value

            if novo_comprimento <= 0 or nova_largura <= 0 or nova_espessura <= 0 or novo_valor_m3 <= 0:
                page.snack_bar = ft.SnackBar(content=ft.Text("Todos os valores devem ser maiores que zero."), bgcolor=ft.colors.RED_700)
                page.snack_bar.open = True
                page.update()
                return

            # Cálculo do volume e custo
            from src.core.orcamento.laje.calculo import calcular_volume_laje

            # Converte valores para Decimal para garantir precisão nos cálculos
            comprimento_dec = Decimal(str(novo_comprimento))
            largura_dec = Decimal(str(nova_largura))
            espessura_dec = Decimal(str(nova_espessura))
            valor_m3_dec = Decimal(str(novo_valor_m3))

            # Calcula o novo volume
            volume = Decimal(str(calcular_volume_laje(float(comprimento_dec), float(largura_dec), float(espessura_dec), novo_tipo_laje)))

            # Calcula o custo total
            custo_total = volume * valor_m3_dec

            # Atualiza a laje no banco de dados
            with postgres.session_scope() as session:
                laje = session.query(Lajes).filter_by(id=laje_id).first()
                if laje:
                    laje.comprimento = comprimento_dec
                    laje.largura = largura_dec
                    laje.espessura = espessura_dec
                    laje.valor_m3 = valor_m3_dec
                    laje.custo_total = custo_total

                    # Adiciona o tipo_laje se a coluna existir
                    if hasattr(laje, "tipo_laje"):
                        laje.tipo_laje = novo_tipo_laje

                    # Adiciona o volume se a coluna existir
                    if hasattr(laje, "volume"):
                        laje.volume = volume

                    # Fecha o diálogo
                    dialog.open = False
                    page.update()

                    # Atualiza o custo estimado do projeto
                    atualizar_custo_estimado(projeto_id)

                    # Exibe mensagem de sucesso
                    page.snack_bar = ft.SnackBar(content=ft.Text("Laje atualizada com sucesso!"), bgcolor=ft.colors.GREEN_700)
                    page.snack_bar.open = True

                    # Recarrega os detalhes do projeto
                    carregar_detalhes_projeto(page, projeto_id)
        except ValueError:
            page.snack_bar = ft.SnackBar(content=ft.Text("Por favor, informe valores numéricos válidos."), bgcolor=ft.colors.RED_700)
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao atualizar laje: {e}"), bgcolor=ft.colors.RED_700)
            page.snack_bar.open = True
            page.update()

    # Função para fechar o diálogo
    def fechar_dialogo(e):
        dialog.open = False
        page.update()

    # Criação do diálogo
    dialog = ft.AlertDialog(
        modal=True,
        title=titulo,
        content=ft.Column(
            [
                ft.Row([comprimento_field, largura_field], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=10),
                ft.Row([espessura_field, valor_m3_field], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=10),
                tipo_laje_dropdown,
                ft.Container(height=10),
            ],
            spacing=10,
            width=500,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar_dialogo),
            ft.TextButton("Salvar", on_click=salvar_alteracoes),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Exibe o diálogo
    page.dialog = dialog
    dialog.open = True
    page.update()
