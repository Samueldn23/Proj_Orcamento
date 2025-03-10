"""Conexão com PostgreSQL"""

import time
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import (
    Session as SQLAlchemySession,
    sessionmaker,
)

from ...config.settings import settings


class PostgresConnection:
    """Gerenciador de conexão PostgreSQL"""

    _instance = None
    _engine = None
    _session_maker = None
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # segundos

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa a conexão"""
        self._engine = create_engine(
            settings.database_url,
            echo=False,
            pool_pre_ping=True,  # Verifica a conexão antes de usar
            pool_recycle=3600,  # Recicla conexões depois de 1 hora
            pool_size=5,  # Tamanho do pool de conexões
            max_overflow=10,  # Conexões adicionais permitidas
        )
        self._session_maker = sessionmaker(bind=self._engine)

    def get_session(self) -> SQLAlchemySession:
        """Retorna uma nova sessão"""
        return self._session_maker()

    @contextmanager
    def session_scope(self, auto_close=True):
        """Fornece um escopo de transação com reconexão automática.

        Args:
            auto_close: Se True, fecha a sessão automaticamente. Se False, deixa a sessão aberta.
        """
        session = self.get_session()
        retries = 0

        while True:
            try:
                yield session
                if auto_close:
                    session.commit()
                break
            except OperationalError as e:
                # Verifica se é erro de conexão fechada
                if "server closed the connection" in str(e) and retries < self.MAX_RETRIES:
                    print(f"Conexão fechada. Tentando reconectar... (Tentativa {retries + 1}/{self.MAX_RETRIES})")
                    session.rollback()
                    retries += 1
                    time.sleep(self.RETRY_DELAY)

                    # Forçar reinicialização da conexão
                    self._initialize()
                    session = self.get_session()
                else:
                    print(f"Erro de conexão: {e}")
                    session.rollback()
                    raise
            except SQLAlchemyError as e:
                print(f"Erro de banco de dados: {e}")
                session.rollback()
                raise
            finally:
                if retries >= self.MAX_RETRIES or (auto_close and retries < self.MAX_RETRIES):
                    session.close()

    @property
    def engine(self):
        """Retorna o engine SQLAlchemy"""
        return self._engine


postgres = PostgresConnection()
Session = postgres.get_session
