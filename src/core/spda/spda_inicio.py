import flet as ft

from src.custom.styles_utils import get_style_manager
from src.navigation.router import navegar_orcamento

gsm = get_style_manager()


def mostrar_inspecao(page):
    page.controls.clear()
    page.title = "Inspeção"

    # Campos de entrada para dados da edificação
    razao_social = ft.TextField(label="Razão Social", width=300)
    endereco = ft.TextField(label="Endereço", width=300)
    telefone = ft.TextField(label="Telefone", width=300)
    email = ft.TextField(label="E-mail", width=300)

    # Campos de inspeção
    tecnico = ft.TextField(label="Nome do Técnico", width=300)
    observacoes = ft.TextField(label="Observações", width=300)

    # Campos para cada item de inspeção com checkbox para "Conforme" ou "Não Conforme"
    item1 = ft.Checkbox(label="1.1 Verificar exigência do SPDA no projeto")
    item2 = ft.Checkbox(label="2.1 Tipo de SPDA")
    # Adicione outros itens conforme o check-list

    # Botão para salvar a inspeção
    salvar_button = gsm.create_button(
        text="Salvar Inspeção",
        on_click=lambda e: salvar_inspecao(
            razao_social.value,
            endereco.value,
            telefone.value,
            email.value,
            tecnico.value,
            observacoes.value,
            [item1.value, item2.value],
        ),
        width=150,
    )

    btn_voltar = gsm.create_button(
        text="Voltar",
        on_click=lambda _: navegar_orcamento(page),
        icon=ft.Icons.ARROW_BACK,
        hover_color=gsm.colors.VOLTAR,
        width=130,
    )

    page.add(
        razao_social,
        endereco,
        telefone,
        email,
        tecnico,
        observacoes,
        item1,
        item2,
        salvar_button,
        btn_voltar,
    )
    page.update()


def salvar_inspecao(razao_social, endereco, telefone, email, tecnico, observacoes, itens):
    # Função que salva a inspeção no banco de dados usando os modelos definidos
    print("Salvando inspeção...")
    # Adicione lógica para salvar no banco
