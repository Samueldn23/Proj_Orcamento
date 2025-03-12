import flet as ft

from src.core.projeto.construcao import Construcao


class Laje(Construcao):
    """Classe para representar uma laje"""

    def __init__(
        self,
        id=None,
        projeto_id=None,
        comprimento=None,
        largura=None,
        altura=None,
        tipo_laje=None,
        caracteristica=None,
        tipo_telha=None,
        comprimento_apoio=None,
        distancia_apoios=None,
        comprimento_de_distribuicao=None,
        comprimento_acrescimo_engaste=None,
    ):
        """Inicializa uma laje"""
        super().__init__(id, projeto_id, comprimento, largura, altura)
        self.tipo_laje = tipo_laje
        self.caracteristica = caracteristica
        self.tipo_telha = tipo_telha
        self.comprimento_apoio = comprimento_apoio
        self.distancia_apoios = distancia_apoios
        self.comprimento_de_distribuicao = comprimento_de_distribuicao
        self.comprimento_acrescimo_engaste = comprimento_acrescimo_engaste

    def realizar_exclusao(self, page):
        """Realiza a exclusão da laje no banco de dados"""
        import time

        from sqlalchemy import text

        from src.core.projeto.detalhes_projeto import tela_detalhes_projeto
        from src.infrastructure.database.connections.postgres import postgres
        from src.infrastructure.database.models.construcoes import Lajes
        from src.infrastructure.database.repositories import RepositorioCliente, RepositorioProjeto

        print(f"[DEBUG] Método realizar_exclusao chamado para Laje, ID={self.id}")
        print(f"[DEBUG] Page disponível: {page is not None}")

        # Verificação adicional para garantir que temos uma página válida
        if page is None:
            print("ERRO CRÍTICO: Page é None, não é possível continuar com a exclusão")
            return

        # Mostrar mensagem de processamento
        if hasattr(page, "snack_bar") and hasattr(page, "update"):
            page.snack_bar = ft.SnackBar(content=ft.Text("Excluindo laje..."), bgcolor=ft.colors.BLUE_700)
            page.snack_bar.open = True
            page.update()

        try:
            # Executa a exclusão diretamente via SQL para garantir
            print("[DEBUG] Executando exclusão direta via SQL")
            with postgres.session_scope() as session:
                # Primeiro obtém o projeto_id para posterior atualização da interface
                laje = session.query(Lajes).filter_by(id=self.id).first()
                if not laje:
                    print("[DEBUG] Laje não encontrada no banco de dados")
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

                print("[DEBUG] Exclusão realizada com sucesso")

                # Verifica se a exclusão foi bem-sucedida usando o método delete para maior segurança
                print("[DEBUG] Verificando exclusão com ORM")
                verificacao = session.query(Lajes).filter_by(id=self.id).first()
                if verificacao:
                    print("[ALERTA] Laje ainda existe! Tentando excluir com ORM diretamente")
                    session.delete(verificacao)
                    session.commit()

                # NOVA ABORDAGEM PARA ATUALIZAÇÃO DA INTERFACE
                if hasattr(page, "snack_bar") and hasattr(page, "update"):
                    # Primeiro exibe a mensagem de sucesso
                    page.snack_bar = ft.SnackBar(content=ft.Text("Laje excluída com sucesso!"), bgcolor=ft.colors.GREEN_700)
                    page.snack_bar.open = True
                    page.update()

                    # Aguarda brevemente para a mensagem ser vista
                    time.sleep(0.5)

                    # Limpa completamente a página para recarregar do zero
                    print("[DEBUG] Limpando página para recarregar completamente")
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
                        print("[DEBUG] Recarregando tela_detalhes_projeto com dados atualizados")
                        tela_detalhes_projeto(page, projeto_atualizado, cliente)

                        # Força mais uma atualização
                        page.update()
                        print("[DEBUG] Página recarregada completamente após exclusão")
                    else:
                        print("[ERRO] Não foi possível encontrar o projeto atualizado")

        except Exception as e:
            print(f"[DEBUG] Erro ao excluir laje: {e}")
            import traceback

            print(traceback.format_exc())

            # Tenta uma abordagem alternativa usando ORM diretamente
            try:
                print("[DEBUG] Tentando abordagem alternativa com ORM")
                with postgres.session_scope() as session:
                    laje = session.query(Lajes).filter_by(id=self.id).first()
                    if laje:
                        projeto_id = laje.projeto_id
                        print(f"[DEBUG] Excluindo laje com ORM, ID={self.id}")
                        session.delete(laje)
                        session.commit()

                        # NOVA ABORDAGEM PARA ATUALIZAÇÃO DA INTERFACE (mesmo no caminho alternativo)
                        if hasattr(page, "snack_bar") and hasattr(page, "update"):
                            page.snack_bar = ft.SnackBar(content=ft.Text("Laje excluída com sucesso!"), bgcolor=ft.colors.GREEN_700)
                            page.snack_bar.open = True
                            page.update()

                            # Aguarda brevemente para a mensagem ser vista
                            time.sleep(0.5)

                            # Limpa completamente a página para recarregar do zero
                            print("[DEBUG] Limpando página para recarregar completamente")
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
                                print("[DEBUG] Recarregando tela_detalhes_projeto com dados atualizados")
                                tela_detalhes_projeto(page, projeto_atualizado, cliente)

                                # Força mais uma atualização
                                page.update()
                                print("[DEBUG] Página recarregada completamente após exclusão")
                            else:
                                print("[ERRO] Não foi possível encontrar o projeto atualizado")
                            return
            except Exception as orm_error:
                print(f"[DEBUG] Erro na abordagem alternativa com ORM: {orm_error}")

            # Mostra mensagem de erro
            if hasattr(page, "snack_bar") and hasattr(page, "update"):
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao excluir laje: {e}"), bgcolor=ft.colors.RED_700)
                page.snack_bar.open = True
                page.update()
