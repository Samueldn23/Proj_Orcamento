"""Módulo para exibir e gerenciar detalhes de um projeto"""

import locale
from decimal import Decimal

import flet as ft

from src.core.projeto import listar_projetos
from src.core.projeto.projeto_utils import atualizar_custo_estimado
from src.custom.styles_utils import get_style_manager
from src.infrastructure.database.connections import Session, postgres
from src.infrastructure.database.models.construcoes import Lajes, Paredes
from src.infrastructure.database.repositories import RepositorioProjeto
from src.navigation.router import navegar_orcamento

# Configurações iniciais
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
gsm = get_style_manager()
repositorio_projeto = RepositorioProjeto()
session = Session()


def tela_detalhes_projeto(page: ft.Page, projeto, cliente):
    # Importação dinâmica para evitar circular import
    from src.core.projeto.construcao import Laje, Parede

    # Atualiza o projeto com os dados mais recentes do banco de dados
    projeto_atualizado = repositorio_projeto.get_by_id(projeto.id)
    if projeto_atualizado:
        projeto = projeto_atualizado
        print(f"Projeto atualizado - ID: {projeto.id}, Nome: {projeto.nome}, Custo: {projeto.custo_estimado}")

    def confirmar_exclusao(e):
        """Exibe diálogo de confirmação para exclusão"""

        def excluir_confirmado(e):
            dlg_confirmacao.open = False
            page.update()
            try:
                if repositorio_projeto.delete(projeto.id):
                    page.open(
                        ft.SnackBar(
                            content=ft.Text("Projeto excluído com sucesso!"),
                            bgcolor=ft.Colors.GREEN,
                        )
                    )
                    listar_projetos.projetos_cliente(page, cliente)
                else:
                    page.open(
                        ft.SnackBar(
                            content=ft.Text("Erro ao excluir projeto!"),
                            bgcolor=ft.Colors.ERROR,
                        )
                    )
            except Exception as error:
                page.open(
                    ft.SnackBar(
                        content=ft.Text(f"Erro ao excluir projeto: {error!s}"),
                        bgcolor=ft.Colors.ERROR,
                    )
                )
            page.update()

        def cancelar_exclusao(e):
            dlg_confirmacao.open = False
            page.update()

        dlg_confirmacao = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(f"Deseja realmente excluir o projeto '{projeto.nome}'?\nEsta ação não poderá ser desfeita!"),
            actions=[
                ft.TextButton("Sim", on_click=excluir_confirmado),
                ft.TextButton("Não", on_click=cancelar_exclusao),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dlg_confirmacao)
        dlg_confirmacao.open = True
        page.update()

    def salvar_edicao(e):
        """Função para salvar as alterações no projeto"""
        try:
            if not nome_input.value:
                page.open(ft.SnackBar(content=ft.Text("Nome do projeto é obrigatório!")))
                return

            # Processamento do custo estimado
            custo_estimado = None
            # Ignora o valor do campo valor_input pois é somente leitura
            # Mantém o valor atual do banco de dados
            if projeto.custo_estimado:
                custo_estimado = projeto.custo_estimado
                print(f"Mantendo custo estimado existente: {custo_estimado}")

            projeto_atualizado = repositorio_projeto.update(
                projeto_id=projeto.id,
                nome=nome_input.value,
                descricao=descricao_input.value,
                custo_estimado=custo_estimado,
            )

            if projeto_atualizado:
                atualizar_custo_estimado(projeto.id)  # Atualiza o custo estimado
                page.open(
                    ft.SnackBar(
                        content=ft.Text("Projeto atualizado com sucesso!"),
                        bgcolor=ft.Colors.GREEN,
                    )
                )
                listar_projetos.projetos_cliente(page, cliente)
            else:
                page.open(
                    ft.SnackBar(
                        content=ft.Text("Erro ao atualizar projeto!"),
                        bgcolor=ft.Colors.ERROR,
                    )
                )
        except ValueError:
            page.open(
                ft.SnackBar(
                    content=ft.Text("Valor inválido para o custo estimado!"),
                    bgcolor=ft.Colors.ERROR,
                )
            )
        except Exception as error:
            page.open(
                ft.SnackBar(
                    content=ft.Text(f"Erro ao atualizar projeto: {error!s}"),
                    bgcolor=ft.Colors.ERROR,
                )
            )
        page.update()

    # Campos de edição
    nome_input = ft.TextField(label="Nome do Projeto", value=projeto.nome, prefix_icon=ft.Icons.FOLDER_SPECIAL, height=50, **gsm.input_style)

    descricao_input = ft.TextField(
        label="Descrição",
        value=projeto.descricao,
        prefix_icon=ft.Icons.DESCRIPTION,
        multiline=True,
        min_lines=2,
        max_lines=3,
        **gsm.input_style,
    )

    # Handlers para os campos
    def on_nome_change(e):
        print(f"Nome alterado para: '{nome_input.value}'")
        page.update()

    def on_descricao_change(e):
        print(f"Descrição alterada para: '{descricao_input.value}'")
        page.update()

    # Configurar os handlers
    nome_input.on_change = on_nome_change
    descricao_input.on_change = on_descricao_change

    # Campo para o valor/custo
    valor_input = ft.TextField(
        label="Custo Estimado (R$)",
        prefix_icon=ft.Icons.ATTACH_MONEY,
        keyboard_type=ft.KeyboardType.NUMBER,
        height=50,
        width=250,
        read_only=True,  # Campo somente leitura
        value=str(projeto.custo_estimado) if projeto.custo_estimado else "",
        # bgcolor=ft.Colors.GREY_50,  # Fundo sutilmente diferente para indicar que é somente leitura
        tooltip="Este valor é calculado automaticamente com base nas construções adicionadas",
        # border_color=ft.Colors.BLUE_200,
        **gsm.input_style,
    )

    # Interface do campo de custo com texto explicativo
    valor_container = ft.Column(
        [
            ft.Text("Custo Estimado", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            ft.Row(
                [
                    valor_input,
                    ft.Row(
                        [
                            gsm.create_button(
                                icon=ft.Icons.SAVE,
                                on_click=salvar_edicao,
                                hover_color=ft.Colors.GREEN_700,
                            ),
                            gsm.create_button(
                                icon=ft.Icons.DELETE_FOREVER,
                                on_click=confirmar_exclusao,
                                hover_color=ft.Colors.RED_700,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                ]
            ),
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.INFO_OUTLINE, color=ft.Colors.GREY_500, size=15),
                        ft.Text(
                            "Valor calculado automaticamente a partir das construções",
                            italic=True,
                            color=ft.Colors.GREY_700,
                            size=12,
                        ),
                    ],
                    spacing=5,
                ),
                margin=ft.margin.only(top=5, left=5),
            ),
        ],
        spacing=5,
    )

    # Adicionar lista de construções
    construcoes_parede = []
    construcoes_laje = []

    # Usa session_scope para obter as construções com reconexão automática
    with postgres.session_scope() as session:
        # Busca as construções do banco
        paredes_originais = session.query(Paredes).filter_by(projeto_id=projeto.id).all()
        lajes_originais = session.query(Lajes).filter_by(projeto_id=projeto.id).all()

        # Desacopla os objetos Paredes
        for parede in paredes_originais:
            # Carrega todos os atributos necessários
            area = parede.area
            custo_total = parede.custo_total
            tipo_tijolo = parede.tipo_tijolo
            quantidade_tijolos = parede.quantidade_tijolos
            parede_id = parede.id

            # Armazena como uma tupla de valores (não depende da sessão)
            construcoes_parede.append(
                {"id": parede_id, "area": area, "custo_total": custo_total, "tipo_tijolo": tipo_tijolo, "quantidade_tijolos": quantidade_tijolos}
            )

        # Desacopla os objetos Lajes
        for laje in lajes_originais:
            # Carrega todos os atributos necessários
            comprimento = laje.comprimento
            largura = laje.largura
            custo_total = laje.custo_total
            espessura = laje.espessura
            laje_id = laje.id

            # Tenta obter atributos opcionais
            tipo_laje = getattr(laje, "tipo_laje", None)
            volume = getattr(laje, "volume", None)

            if volume is None:
                # Calcula o volume se não estiver disponível
                volume = comprimento * largura * espessura * Decimal("0.01")

            # Armazena como um dicionário (não depende da sessão)
            construcoes_laje.append(
                {
                    "id": laje_id,
                    "comprimento": comprimento,
                    "largura": largura,
                    "custo_total": custo_total,
                    "tipo_laje": tipo_laje,
                    "volume": volume,
                    "area": comprimento * largura,
                }
            )

    # Calcula se existem construções de qualquer tipo
    tem_construcoes = bool(construcoes_parede) or bool(construcoes_laje)

    # Cria um card para o título da seção de construções
    titulo_construcoes = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CONSTRUCTION, color=ft.Colors.BLUE_700),
                ft.Text("Construções", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            ],
            spacing=10,
        ),
        padding=ft.padding.only(left=10, top=15, bottom=10),
    )

    # Lista de construções com estilo aprimorado
    lista_construcoes = (
        ft.Container(
            content=ft.Column(
                [
                    titulo_construcoes,
                    ft.Divider(height=1, color=ft.Colors.BLUE_100),
                    ft.Container(
                        content=ft.Column(
                            # Lista de paredes
                            [
                                Parede(p["area"], p["custo_total"], p["tipo_tijolo"], p["quantidade_tijolos"], p["id"], projeto.id).criar_card()
                                for p in construcoes_parede
                            ]
                            +
                            # Lista de lajes
                            [Laje(l["area"], l["custo_total"], l["tipo_laje"], l["volume"], l["id"], projeto.id).criar_card() for l in construcoes_laje]
                        ),
                        padding=10,
                    ),
                ],
                spacing=0,
            ),
            border=ft.border.all(1, ft.Colors.BLUE_100),
            border_radius=8,
            margin=ft.margin.only(top=10),
        )
        if tem_construcoes
        else ft.Container(
            content=ft.Column(
                [
                    titulo_construcoes,
                    ft.Divider(height=1, color=ft.Colors.BLUE_100),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.INFO_OUTLINE, color=ft.Colors.GREY_400, size=20),
                                ft.Text("Nenhuma construção cadastrada", color=ft.Colors.GREY_600),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.symmetric(vertical=30),
                        width=float("inf"),
                    ),
                ]
            ),
            border=ft.border.all(1, ft.Colors.BLUE_100),
            border_radius=8,
            margin=ft.margin.only(top=10),
        )
    )

    # Título e metadados do projeto
    cabecalho = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.FOLDER_SPECIAL, color=ft.Colors.BLUE_700, size=24),
                        ft.Text(
                            "Detalhes do Projeto",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.CALENDAR_TODAY, color=ft.Colors.GREY_700, size=16),
                            ft.Text(
                                f"Criado em: {projeto.criado_em.strftime('%d/%m/%Y')}",
                                color=ft.Colors.WHITE70,
                                size=12,
                            ),
                            ft.VerticalDivider(width=1, color=ft.Colors.GREY_400),
                            ft.Text(
                                f"Atualizado: {projeto.atualizado_em.strftime('%d/%m/%Y')}",
                                color=ft.Colors.WHITE70,
                                size=12,
                            ),
                        ],
                        spacing=5,
                    ),
                    margin=ft.margin.only(top=5),
                ),
            ],
        ),
        padding=ft.padding.all(15),
        bgcolor=ft.Colors.GREY_900,
        border_radius=8,
        border=ft.border.all(1, ft.Colors.GREY_900),
    )

    # Card de formulário
    card_formulario = ft.Container(
        content=ft.Column(
            [
                # ft.Text("Informações do Projeto", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                # ft.Divider(height=1, color=ft.Colors.BLUE_100),
                nome_input,
                descricao_input,
                ft.Container(
                    content=valor_container,
                    padding=ft.padding.only(top=5),
                ),
            ],
            spacing=15,
        ),
        padding=20,
        border=ft.border.all(1, ft.Colors.BLUE_100),
        border_radius=8,
        margin=ft.margin.only(top=15, bottom=15),
    )

    # Barra de ações (botões)
    barra_acoes = ft.Container(
        content=ft.Column(
            [
                # ft.Row(
                #    [
                #        gsm.create_button(
                #            text="",
                #            icon=ft.Icons.ADD_HOME_WORK,
                #            on_click=lambda _: navegar_orcamento(page, cliente, projeto),
                #            hover_color=ft.Colors.BLUE_700,
                #        ),
                #        gsm.create_button(
                #            text="",
                #            icon=ft.Icons.SAVE,
                #            on_click=salvar_edicao,
                #            hover_color=ft.Colors.GREEN_700,
                #        ),
                #    ],
                #    alignment=ft.MainAxisAlignment.CENTER,
                #    spacing=10,
                # ),
                ft.Row(
                    [
                        gsm.create_button(
                            text="Construir",
                            icon=ft.Icons.ADD_HOME_WORK,
                            on_click=lambda _: navegar_orcamento(page, cliente, projeto),
                            hover_color=ft.Colors.BLUE_700,
                        ),
                        gsm.create_button(
                            text="Voltar",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: listar_projetos.projetos_cliente(page, cliente),
                            hover_color=gsm.colors.VOLTAR,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
            ],
            spacing=15,
        ),
        padding=ft.padding.only(bottom=10, top=5),
    )

    # Definição da interface principal
    page.window_resizable = True
    page.controls.clear()
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    cabecalho,
                    card_formulario,
                    barra_acoes,
                    lista_construcoes,
                ],
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                spacing=0,
            ),
            padding=15,
            border_radius=8,
        )
    )
    page.update()


def carregar_detalhes_projeto(page, projeto_id):
    """
    Carrega os detalhes do projeto e exibe na página.
    Função auxiliar para recarregar a página após edições ou exclusões.
    """
    print(f"[DEBUG] Iniciando carregar_detalhes_projeto para projeto_id={projeto_id}")
    print(f"[DEBUG] Page: {page}")

    if page is None:
        print("[DEBUG] ERRO: Page é None em carregar_detalhes_projeto!")
        return

    if not hasattr(page, "update"):
        print("[DEBUG] ERRO: Page não possui método update em carregar_detalhes_projeto!")
        return

    try:
        # Buscar o projeto atualizado
        print(f"[DEBUG] Buscando projeto com ID={projeto_id}")
        projeto = repositorio_projeto.get_by_id(projeto_id)
        print(f"[DEBUG] Projeto encontrado: {projeto is not None}")

        if projeto:
            # Buscar dados do cliente associado ao projeto
            from src.infrastructure.database.repositories import RepositorioCliente

            print(f"[DEBUG] Buscando dados do cliente com ID={projeto.cliente_id}")
            cliente_repo = RepositorioCliente()
            cliente = cliente_repo.get_by_id(projeto.cliente_id)
            print(f"[DEBUG] Cliente encontrado: {cliente is not None}")

            # Exibir a tela de detalhes com os dados atualizados
            print(f"[DEBUG] Chamando tela_detalhes_projeto com projeto_id={projeto_id}")
            tela_detalhes_projeto(page, projeto, cliente)
            print("[DEBUG] tela_detalhes_projeto concluído")
        else:
            # Se o projeto não for encontrado, mostrar mensagem e voltar para a lista
            print(f"[DEBUG] Projeto não encontrado com ID={projeto_id}")
            page.snack_bar = ft.SnackBar(content=ft.Text("Projeto não encontrado."), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            page.update()

            # Volta para a lista de projetos
            from src.core.cliente.clientes import tela_clientes

            print("[DEBUG] Voltando para a tela_clientes")
            tela_clientes(page)

    except Exception as e:
        print(f"[DEBUG] Exceção em carregar_detalhes_projeto: {e}")
        import traceback

        print(f"[DEBUG] Traceback: {traceback.format_exc()}")

        # Tentar exibir mensagem de erro para o usuário
        try:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao carregar detalhes: {e}"), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            page.update()
        except Exception as ui_error:
            print(f"[DEBUG] Não foi possível exibir erro na interface: {ui_error}")
