import locale

import flet as ft

# Configuração da localização para formatação de moeda
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


class Construcao:
    """Classe base para diferentes tipos de construção"""

    def __init__(self, tipo, area, custo_total, id=None, projeto_id=None):
        self.tipo = tipo
        self.area = area
        self.custo_total = custo_total
        self.id = id
        self.projeto_id = projeto_id

    def criar_card(self):
        """Método para criar um card com informações da construção"""
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        # Ícone com cor baseada no tipo de construção
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.HOUSE_SIDING if self.tipo == "Parede" else ft.Icons.LAYERS if self.tipo == "Laje" else ft.Icons.ELECTRIC_BOLT,
                                color=ft.Colors.WHITE,
                                size=18,
                            ),
                            width=32,
                            height=32,
                            border_radius=ft.border_radius.all(16),
                            bgcolor=ft.Colors.BLUE_600 if self.tipo == "Parede" else ft.Colors.PURPLE_600 if self.tipo == "Laje" else ft.Colors.ORANGE_600,
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
                                    f"Área: {self.area:.2f}m²",
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
                                        data=self,  # Passa a instância atual como data
                                        on_click=lambda e: self.log_e_chamar_editar(e),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_FOREVER,
                                        tooltip="Excluir",
                                        icon_color=ft.Colors.RED_600,
                                        icon_size=20,
                                        data=self,  # Passa a instância atual como data
                                        on_click=lambda e: self.log_e_chamar_excluir(e),
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

    def editar_construcao(self, e):
        """Método base para editar a construção. Deve ser sobrescrito pelas subclasses."""
        print(f"Editar construção base não implementado. Tipo: {self.tipo}, ID: {self.id}")

    def excluir_construcao(self, e):
        """Confirma e exclui a parede"""
        print(f"Tentando excluir parede: ID={self.id}, Projeto ID={self.projeto_id}")
        print(f"Dados do evento: control={getattr(e, 'control', None)}, page={hasattr(e, 'page')}")

        # Verificar se temos o ID da parede
        if not self.id:
            print(f"ERRO: ID da parede não encontrado")
            return

        # Tentamos obter a página da maneira mais confiável
        if hasattr(e, "page") and e.page is not None:
            print(f"Usando página do evento para excluir parede. ID={self.id}")
            self.exibir_dialogo_confirmacao(e.page)
            return

        # Se não houver página no evento, tentamos através do control
        if hasattr(e, "control") and hasattr(e.control, "page"):
            print(f"Usando página do control para excluir parede. ID={self.id}")
            self.exibir_dialogo_confirmacao(e.control.page)
            return

        print(f"ERRO: Não foi possível obter a página para excluir parede. ID={self.id}")

    def exibir_dialogo_confirmacao(self, page):
        """Exibe um diálogo de confirmação para exclusão"""
        print(f"Iniciando confirmação de exclusão para {self.tipo}, ID={self.id}")
        print(f"Page overlay disponível: {hasattr(page, 'overlay')}")

        # Armazenamos self em uma variável para evitar problemas de escopo
        instancia_atual = self

        def fechar_dialogo(e):
            print(f"Fechando diálogo de exclusão para {instancia_atual.tipo}, ID={instancia_atual.id}")
            dlg_confirmacao.open = False
            page.update()

        def confirmar_exclusao(e):
            print(f"[INÍCIO] Confirmando exclusão para {instancia_atual.tipo}, ID={instancia_atual.id}")
            # Fechamos o diálogo primeiro
            dlg_confirmacao.open = False
            page.update()

            try:
                # Executamos a exclusão
                print(f"Executando exclusão de {instancia_atual.tipo}, ID={instancia_atual.id}")
                instancia_atual.realizar_exclusao(page)
                print(f"Exclusão concluída com sucesso")
            except Exception as erro:
                print(f"ERRO AO EXCLUIR: {erro}")
                import traceback

                print(traceback.format_exc())

                # Exibe mensagem de erro
                if hasattr(page, "snack_bar") and hasattr(page, "update"):
                    page.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao excluir {instancia_atual.tipo.lower()}: {erro}"), bgcolor=ft.Colors.RED)
                    page.snack_bar.open = True
                    page.update()

        # Limpa todos os diálogos anteriores do overlay
        if hasattr(page, "overlay"):
            # Guarda uma cópia dos itens que não são diálogos
            itens_nao_dialogo = [item for item in page.overlay if not isinstance(item, ft.AlertDialog)]
            # Limpa o overlay e restaura apenas os itens que não são diálogos
            page.overlay.clear()
            for item in itens_nao_dialogo:
                page.overlay.append(item)
            page.update()

        # Criamos o diálogo com botões de confirmação e cancelamento
        print(f"Criando diálogo de confirmação")
        dlg_confirmacao = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Excluir {self.tipo}", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Text(f"Deseja realmente excluir esta {self.tipo.lower()}?\nEsta ação não poderá ser desfeita!", size=16),
            actions=[
                ft.TextButton("Não", on_click=fechar_dialogo),
                ft.ElevatedButton(
                    "Sim",
                    on_click=confirmar_exclusao,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.RED,
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Adicionamos o diálogo ao overlay da página
        print(f"Adicionando diálogo ao overlay da página")
        if hasattr(page, "overlay"):
            page.overlay.append(dlg_confirmacao)
            dlg_confirmacao.open = True
            page.update()
            print(f"Diálogo adicionado ao overlay e aberto")
        else:
            print(f"ERRO: Page não possui overlay")
            # Tentativa alternativa usando page.dialog
            page.dialog = dlg_confirmacao
            dlg_confirmacao.open = True
            page.update()
            print(f"Tentativa alternativa: usando page.dialog")

    def realizar_exclusao(self, page):
        """Método para realizar a exclusão efetiva. Deve ser implementado pelas subclasses."""
        print(f"Exclusão não implementada para {self.tipo}, ID={self.id}")

    def log_e_chamar_editar(self, e):
        """Método auxiliar para registrar logs e chamar o método editar_construcao"""
        print(f"Clique no botão EDITAR para {self.tipo}, ID={self.id}")
        print(f"Dados do evento: control={type(getattr(e, 'control', None))}, page={type(getattr(e, 'page', None))}")
        print(f"Objeto data no control: {getattr(getattr(e, 'control', None), 'data', None)}")

        # Importante: Estamos usando o e.page que é fornecido pelo Flet no evento
        # e não e.control.data que pode estar incorreto
        if hasattr(e, "page") and e.page is not None:
            # Clone o evento e adicione a página correta
            self.editar_construcao(e)
        else:
            print(f"ERRO: Página não encontrada no evento para editar {self.tipo}")
            # Tente encontrar a página através do control
            if hasattr(e, "control") and hasattr(e.control, "page"):
                print(f"Tentando usar a página do control para editar")
                # Chamamos diretamente os métodos específicos para cada tipo
                if self.tipo == "Parede":
                    from src.core.orcamento.paredes import editar_parede

                    editar_parede(e.control.page, self.id, self.projeto_id)
                elif self.tipo == "Laje":
                    from src.core.orcamento.laje.calculos import editar_laje

                    editar_laje(e.control.page, self.id, self.projeto_id)

    def log_e_chamar_excluir(self, e):
        """Método auxiliar para registrar logs e chamar o método excluir_construcao"""
        print(f"Clique no botão EXCLUIR para {self.tipo}, ID={self.id}")
        print(f"Dados do evento: control={type(getattr(e, 'control', None))}, page={type(getattr(e, 'page', None))}")
        print(f"Objeto data no control: {getattr(getattr(e, 'control', None), 'data', None)}")

        # Importante: Estamos usando o e.page que é fornecido pelo Flet no evento
        if hasattr(e, "page") and e.page is not None:
            self.excluir_construcao(e)
        else:
            print(f"ERRO: Página não encontrada no evento para excluir {self.tipo}")
            # Tente encontrar a página através do control
            if hasattr(e, "control") and hasattr(e.control, "page"):
                print(f"Tentando usar a página do control para excluir")
                e.page = e.control.page  # Adicione a página ao evento
                self.excluir_construcao(e)


class Parede(Construcao):
    def __init__(self, area, custo_total, tipo_tijolo, quantidade_tijolos, id=None, projeto_id=None):
        super().__init__("Parede", area, custo_total, id, projeto_id)
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

    def editar_construcao(self, e):
        """Abre o diálogo para editar a parede"""
        from src.core.orcamento.paredes import editar_parede

        print(f"Tentando editar parede: ID={self.id}, Projeto ID={self.projeto_id}")
        print(f"Dados do evento: control={getattr(e, 'control', None)}, page={hasattr(e, 'page')}")

        # Verificar se temos todos os dados necessários
        if not self.id or not self.projeto_id:
            print(f"ERRO: Dados insuficientes para editar parede. ID={self.id}, Projeto ID={self.projeto_id}")
            return

        # Tentamos obter a página da maneira mais confiável
        if hasattr(e, "page") and e.page is not None:
            print(f"Usando página do evento para editar parede. ID={self.id}")
            editar_parede(e.page, self.id, self.projeto_id)
            return

        # Se não houver página no evento, tentamos outras maneiras de obter
        if hasattr(e, "control") and hasattr(e.control, "page"):
            print(f"Usando página do control para editar parede. ID={self.id}")
            editar_parede(e.control.page, self.id, self.projeto_id)
            return

        print(f"ERRO: Não foi possível obter a página para editar parede. ID={self.id}")

    def excluir_construcao(self, e):
        """Confirma e exclui a parede"""
        print(f"Tentando excluir parede: ID={self.id}, Projeto ID={self.projeto_id}")
        print(f"Dados do evento: control={getattr(e, 'control', None)}, page={hasattr(e, 'page')}")

        # Verificar se temos o ID da parede
        if not self.id:
            print(f"ERRO: ID da parede não encontrado")
            return

        # Tentamos obter a página da maneira mais confiável
        if hasattr(e, "page") and e.page is not None:
            print(f"Usando página do evento para excluir parede. ID={self.id}")
            self.exibir_dialogo_confirmacao(e.page)
            return

        # Se não houver página no evento, tentamos através do control
        if hasattr(e, "control") and hasattr(e.control, "page"):
            print(f"Usando página do control para excluir parede. ID={self.id}")
            self.exibir_dialogo_confirmacao(e.control.page)
            return

        print(f"ERRO: Não foi possível obter a página para excluir parede. ID={self.id}")

    def realizar_exclusao(self, page):
        """Realiza a exclusão da parede no banco de dados"""
        import time

        from sqlalchemy import text

        from src.core.projeto.detalhes_projeto import carregar_detalhes_projeto, tela_detalhes_projeto
        from src.infrastructure.database.connections.postgres import postgres
        from src.infrastructure.database.models.construcoes import Paredes
        from src.infrastructure.database.repositories import RepositorioCliente, RepositorioProjeto

        print(f"[DEBUG] Método realizar_exclusao chamado para Parede, ID={self.id}")
        print(f"[DEBUG] Page disponível: {page is not None}")

        # Verificação adicional para garantir que temos uma página válida
        if page is None:
            print(f"ERRO CRÍTICO: Page é None, não é possível continuar com a exclusão")
            return

        # Mostrar mensagem de processamento
        if hasattr(page, "snack_bar") and hasattr(page, "update"):
            page.snack_bar = ft.SnackBar(content=ft.Text("Excluindo parede..."), bgcolor=ft.colors.BLUE_700)
            page.snack_bar.open = True
            page.update()

        try:
            # Executa a exclusão diretamente via SQL para garantir
            print(f"[DEBUG] Executando exclusão direta via SQL")
            with postgres.session_scope() as session:
                # Primeiro obtém o projeto_id para posterior atualização da interface
                parede = session.query(Paredes).filter_by(id=self.id).first()
                if not parede:
                    print(f"[DEBUG] Parede não encontrada no banco de dados")
                    if hasattr(page, "snack_bar") and hasattr(page, "update"):
                        page.snack_bar = ft.SnackBar(content=ft.Text("Parede não encontrada no banco de dados"), bgcolor=ft.colors.RED_700)
                        page.snack_bar.open = True
                        page.update()
                    return

                projeto_id = parede.projeto_id
                print(f"[DEBUG] Projeto ID obtido: {projeto_id}")

                # Executa o DELETE direto para garantir exclusão
                sql = text(f"DELETE FROM paredes WHERE id = {self.id}")
                print(f"[DEBUG] Executando SQL: {sql}")
                session.execute(sql)
                session.commit()

                print(f"[DEBUG] Exclusão realizada com sucesso")

                # Verifica se a exclusão foi bem-sucedida usando o método delete para maior segurança
                print(f"[DEBUG] Verificando exclusão com ORM")
                verificacao = session.query(Paredes).filter_by(id=self.id).first()
                if verificacao:
                    print(f"[ALERTA] Parede ainda existe! Tentando excluir com ORM diretamente")
                    session.delete(verificacao)
                    session.commit()

                # NOVA ABORDAGEM PARA ATUALIZAÇÃO DA INTERFACE
                if hasattr(page, "snack_bar") and hasattr(page, "update"):
                    # Primeiro exibe a mensagem de sucesso
                    page.snack_bar = ft.SnackBar(content=ft.Text("Parede excluída com sucesso!"), bgcolor=ft.colors.GREEN_700)
                    page.snack_bar.open = True
                    page.update()

                    # Aguarda brevemente para a mensagem ser vista
                    time.sleep(0.5)

                    # Limpa completamente a página para recarregar do zero
                    print(f"[DEBUG] Limpando página para recarregar completamente")
                    page.controls.clear()

                    # Preserva apenas a barra de navegação e appbar, se existirem
                    appbar = page.appbar
                    navigation_bar = page.navigation_bar
                    if appbar:
                        page.appbar = appbar
                    if navigation_bar:
                        page.navigation_bar = navigation_bar

                    page.update()

                    # Busca dados mais atualizados do projeto e cliente
                    print(f"[DEBUG] Buscando dados atualizados para projeto_id={projeto_id}")
                    repo_projeto = RepositorioProjeto()
                    projeto_atualizado = repo_projeto.get_by_id(projeto_id)

                    if projeto_atualizado:
                        repo_cliente = RepositorioCliente()
                        cliente = repo_cliente.get_by_id(projeto_atualizado.cliente_id)

                        # Carrega a tela de detalhes do projeto do zero
                        print(f"[DEBUG] Recarregando tela_detalhes_projeto com dados atualizados")
                        tela_detalhes_projeto(page, projeto_atualizado, cliente)

                        # Força mais uma atualização
                        page.update()
                        print(f"[DEBUG] Página recarregada completamente após exclusão")
                    else:
                        print(f"[ERRO] Não foi possível encontrar o projeto atualizado")

        except Exception as e:
            print(f"[DEBUG] Erro ao excluir parede: {e}")
            import traceback

            print(traceback.format_exc())

            # Tenta uma abordagem alternativa usando ORM diretamente
            try:
                print(f"[DEBUG] Tentando abordagem alternativa com ORM")
                with postgres.session_scope() as session:
                    parede = session.query(Paredes).filter_by(id=self.id).first()
                    if parede:
                        projeto_id = parede.projeto_id
                        print(f"[DEBUG] Excluindo parede com ORM, ID={self.id}")
                        session.delete(parede)
                        session.commit()

                        # NOVA ABORDAGEM PARA ATUALIZAÇÃO DA INTERFACE (mesmo no caminho alternativo)
                        if hasattr(page, "snack_bar") and hasattr(page, "update"):
                            page.snack_bar = ft.SnackBar(content=ft.Text("Parede excluída com sucesso!"), bgcolor=ft.colors.GREEN_700)
                            page.snack_bar.open = True
                            page.update()

                            # Aguarda brevemente para a mensagem ser vista
                            time.sleep(0.5)

                            # Limpa completamente a página para recarregar do zero
                            print(f"[DEBUG] Limpando página para recarregar completamente")
                            page.controls.clear()

                            # Preserva apenas a barra de navegação e appbar, se existirem
                            appbar = page.appbar
                            navigation_bar = page.navigation_bar
                            if appbar:
                                page.appbar = appbar
                            if navigation_bar:
                                page.navigation_bar = navigation_bar

                            page.update()

                            # Busca dados mais atualizados do projeto e cliente
                            print(f"[DEBUG] Buscando dados atualizados para projeto_id={projeto_id}")
                            repo_projeto = RepositorioProjeto()
                            projeto_atualizado = repo_projeto.get_by_id(projeto_id)

                            if projeto_atualizado:
                                repo_cliente = RepositorioCliente()
                                cliente = repo_cliente.get_by_id(projeto_atualizado.cliente_id)

                                # Carrega a tela de detalhes do projeto do zero
                                print(f"[DEBUG] Recarregando tela_detalhes_projeto com dados atualizados")
                                tela_detalhes_projeto(page, projeto_atualizado, cliente)

                                # Força mais uma atualização
                                page.update()
                                print(f"[DEBUG] Página recarregada completamente após exclusão")
                            else:
                                print(f"[ERRO] Não foi possível encontrar o projeto atualizado")
                            return
            except Exception as orm_error:
                print(f"[DEBUG] Erro na abordagem alternativa com ORM: {orm_error}")

            # Mostra mensagem de erro
            if hasattr(page, "snack_bar") and hasattr(page, "update"):
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao excluir parede: {e}"), bgcolor=ft.colors.RED_700)
                page.snack_bar.open = True
                page.update()


class Laje(Construcao):
    def __init__(self, area, custo_total, tipo_laje, volume, id=None, projeto_id=None):
        super().__init__("Laje", area, custo_total, id, projeto_id)
        self.tipo_laje = tipo_laje
        self.volume = volume

    def criar_card(self):
        card = super().criar_card()

        # Adiciona informações específicas sobre a laje em um container separado
        info_container = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.LAYERS, size=14, color=ft.Colors.BLUE_GREY_600),
                                ft.Text(
                                    f"Tipo: {self.tipo_laje or 'Laje Maciça'}",
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
                                ft.Icon(ft.Icons.CIRCLE, size=14, color=ft.Colors.BLUE_GREY_600),
                                ft.Text(
                                    f"Volume: {self.volume:.2f} m³",
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

    def editar_construcao(self, e):
        """Abre o diálogo para editar a laje"""
        from src.core.orcamento.laje.calculos import editar_laje

        print(f"Tentando editar laje: ID={self.id}, Projeto ID={self.projeto_id}")
        print(f"Dados do evento: control={getattr(e, 'control', None)}, page={hasattr(e, 'page')}")

        # Verificar se temos todos os dados necessários
        if not self.id or not self.projeto_id:
            print(f"ERRO: Dados insuficientes para editar laje. ID={self.id}, Projeto ID={self.projeto_id}")
            return

        # Tentamos obter a página da maneira mais confiável
        if hasattr(e, "page") and e.page is not None:
            print(f"Usando página do evento para editar laje. ID={self.id}")
            editar_laje(e.page, self.id, self.projeto_id)
            return

        # Se não houver página no evento, tentamos outras maneiras de obter
        if hasattr(e, "control") and hasattr(e.control, "page"):
            print(f"Usando página do control para editar laje. ID={self.id}")
            editar_laje(e.control.page, self.id, self.projeto_id)
            return

        print(f"ERRO: Não foi possível obter a página para editar laje. ID={self.id}")

    def excluir_construcao(self, e):
        """Confirma e exclui a laje"""
        print(f"Tentando excluir laje: ID={self.id}, Projeto ID={self.projeto_id}")
        print(f"Dados do evento: control={getattr(e, 'control', None)}, page={hasattr(e, 'page')}")
        print(f"Tipo do e.control: {type(getattr(e, 'control', None))}")

        # Verificar se temos o ID da laje
        if not self.id:
            print(f"ERRO: ID da laje não encontrado")
            return

        # Tentamos obter a página da maneira mais confiável
        if hasattr(e, "page") and e.page is not None:
            print(f"Usando página do evento para excluir laje. ID={self.id}")
            self.exibir_dialogo_confirmacao(e.page)
            return

        # Se não houver página no evento, tentamos através do control
        if hasattr(e, "control") and hasattr(e.control, "page"):
            print(f"Usando página do control para excluir laje. ID={self.id}")
            self.exibir_dialogo_confirmacao(e.control.page)
            return

        print(f"ERRO: Não foi possível obter a página para excluir laje. ID={self.id}")

    def realizar_exclusao(self, page):
        """Realiza a exclusão da laje no banco de dados"""
        import time

        from sqlalchemy import text

        from src.core.projeto.detalhes_projeto import carregar_detalhes_projeto
        from src.infrastructure.database.connections.postgres import postgres
        from src.infrastructure.database.models.construcoes import Lajes

        print(f"[DEBUG] Método realizar_exclusao chamado para Laje, ID={self.id}")
        print(f"[DEBUG] Page disponível: {page is not None}")

        # Verificação adicional para garantir que temos uma página válida
        if page is None:
            print(f"ERRO CRÍTICO: Page é None, não é possível continuar com a exclusão")
            return

        # Mostrar mensagem de processamento
        if hasattr(page, "snack_bar") and hasattr(page, "update"):
            page.snack_bar = ft.SnackBar(content=ft.Text("Excluindo laje..."), bgcolor=ft.colors.BLUE_700)
            page.snack_bar.open = True
            page.update()

        try:
            # Executa a exclusão diretamente via SQL para garantir
            print(f"[DEBUG] Executando exclusão direta via SQL")
            with postgres.session_scope() as session:
                # Primeiro obtém o projeto_id para posterior atualização da interface
                laje = session.query(Lajes).filter_by(id=self.id).first()
                if not laje:
                    print(f"[DEBUG] Laje não encontrada no banco de dados")
                    if hasattr(page, "snack_bar") and hasattr(page, "update"):
                        page.snack_bar = ft.SnackBar(content=ft.Text("Laje não encontrada no banco de dados"), bgcolor=ft.colors.RED_700)
                        page.snack_bar.open = True
                        page.update()
                    return

                projeto_id = laje.projeto_id
                print(f"[DEBUG] Projeto ID obtido: {projeto_id}")

                # Executa o DELETE direto para garantir exclusão
                sql = text(f"DELETE FROM lajes WHERE id = {self.id}")
                print(f"[DEBUG] Executando SQL: {sql}")
                session.execute(sql)
                session.commit()

                print(f"[DEBUG] Exclusão realizada com sucesso")

                # Verifica se a exclusão foi bem-sucedida usando o método delete para maior segurança
                print(f"[DEBUG] Verificando exclusão com ORM")
                verificacao = session.query(Lajes).filter_by(id=self.id).first()
                if verificacao:
                    print(f"[ALERTA] Laje ainda existe! Tentando excluir com ORM diretamente")
                    session.delete(verificacao)
                    session.commit()

                # Atualiza a interface - INÍCIO DAS MODIFICAÇÕES
                if hasattr(page, "snack_bar") and hasattr(page, "update"):
                    # Primeiro exibe a mensagem de sucesso
                    page.snack_bar = ft.SnackBar(content=ft.Text("Laje excluída com sucesso!"), bgcolor=ft.colors.GREEN_700)
                    page.snack_bar.open = True
                    page.update()

                    print(f"[DEBUG] Forçando atualização da página após exclusão")

                    # Agora carrega os detalhes atualizados do projeto
                    print(f"[DEBUG] Chamando carregar_detalhes_projeto com projeto_id={projeto_id}")

                    # Limpa a página atual para garantir que tudo seja recarregado
                    if hasattr(page, "controls") and page.controls:
                        print(f"[DEBUG] Limpando controles existentes da página")
                        # Guarda o appbar e o navigation_bar se existirem
                        appbar = page.appbar
                        navigation_bar = page.navigation_bar
                        page.controls.clear()
                        if appbar:
                            page.appbar = appbar
                        if navigation_bar:
                            page.navigation_bar = navigation_bar
                        page.update()

                    # Chama a função para recarregar os detalhes
                    carregar_detalhes_projeto(page, projeto_id)

                    # Força mais uma atualização para garantir
                    page.update()
                    print(f"[DEBUG] Atualização forçada concluída")
                # FIM DAS MODIFICAÇÕES

        except Exception as e:
            print(f"[DEBUG] Erro ao excluir laje: {e}")
            import traceback

            print(traceback.format_exc())

            # Tenta uma abordagem alternativa usando ORM diretamente
            try:
                print(f"[DEBUG] Tentando abordagem alternativa com ORM")
                with postgres.session_scope() as session:
                    laje = session.query(Lajes).filter_by(id=self.id).first()
                    if laje:
                        projeto_id = laje.projeto_id
                        print(f"[DEBUG] Excluindo laje com ORM, ID={self.id}")
                        session.delete(laje)
                        session.commit()

                        # Atualiza a interface
                        if hasattr(page, "snack_bar") and hasattr(page, "update"):
                            page.snack_bar = ft.SnackBar(content=ft.Text("Laje excluída com sucesso!"), bgcolor=ft.colors.GREEN_700)
                            page.snack_bar.open = True

                            # Limpa a página atual para garantir que tudo seja recarregado
                            if hasattr(page, "controls") and page.controls:
                                print(f"[DEBUG] Limpando controles existentes da página")
                                # Guarda o appbar e o navigation_bar se existirem
                                appbar = page.appbar
                                navigation_bar = page.navigation_bar
                                page.controls.clear()
                                if appbar:
                                    page.appbar = appbar
                                if navigation_bar:
                                    page.navigation_bar = navigation_bar
                                page.update()

                            carregar_detalhes_projeto(page, projeto_id)
                            page.update()
                            return
            except Exception as orm_error:
                print(f"[DEBUG] Erro na abordagem alternativa com ORM: {orm_error}")

            # Mostra mensagem de erro
            if hasattr(page, "snack_bar") and hasattr(page, "update"):
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao excluir laje: {e}"), bgcolor=ft.colors.RED_700)
                page.snack_bar.open = True
                page.update()


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
                                        on_click=lambda e: print("editar_construcao(parede)"),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        tooltip="Excluir",
                                        on_click=lambda e: print("excluir_construcao(parede)"),
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


def confirmar_e_realizar_exclusao(instancia, page):
    """
    Função de alto nível para executar a exclusão de uma construção.
    Recebe a instância e a página como parâmetros para evitar problemas de escopo.
    """
    print(f"[ALTO NÍVEL] Iniciando exclusão para {instancia.tipo}, ID={instancia.id}")
    print(f"[ALTO NÍVEL] Tipo da instância: {type(instancia)}")
    print(f"[ALTO NÍVEL] Tipo da página: {type(page)}")

    try:
        print(f"[ALTO NÍVEL] Chamando método realizar_exclusao da instância")
        # Chamando diretamente o método de exclusão da instância passada
        instancia.realizar_exclusao(page)
        print(f"[ALTO NÍVEL] Método realizar_exclusao concluído com sucesso")
        return True
    except Exception as e:
        print(f"[ALTO NÍVEL] Erro ao executar exclusão: {e}")
        print(f"[ALTO NÍVEL] Tipo do erro: {type(e)}")
        import traceback

        print(f"[ALTO NÍVEL] Traceback completo:")
        print(traceback.format_exc())

        # Tenta executar a exclusão diretamente com SQL
        try:
            from sqlalchemy import text

            from src.infrastructure.database.connections.postgres import postgres

            print(f"[ALTO NÍVEL] Tentando exclusão direta via SQL")
            tabela = ""
            if instancia.tipo == "Parede":
                tabela = "paredes"
            elif instancia.tipo == "Laje":
                tabela = "lajes"

            if tabela and instancia.id:
                with postgres.session_scope() as session:
                    sql = text(f"DELETE FROM {tabela} WHERE id = {instancia.id}")
                    print(f"[ALTO NÍVEL] Executando SQL: {sql}")
                    session.execute(sql)
                    session.commit()
                    print(f"[ALTO NÍVEL] Exclusão direta via SQL concluída")

                    # Atualiza a interface se necessário
                    from src.core.projeto.detalhes_projeto import carregar_detalhes_projeto

                    if hasattr(page, "snack_bar") and hasattr(page, "update"):
                        page.snack_bar = ft.SnackBar(content=ft.Text(f"{instancia.tipo} excluído(a) com sucesso!"), bgcolor=ft.colors.GREEN_700)
                        page.snack_bar.open = True
                        if hasattr(instancia, "projeto_id") and instancia.projeto_id:
                            carregar_detalhes_projeto(page, instancia.projeto_id)
                    return True
        except Exception as e2:
            print(f"[ALTO NÍVEL] Erro na tentativa de exclusão via SQL: {e2}")

        return False
