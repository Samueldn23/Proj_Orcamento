"""Conexão com PostgreSQL"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession
from ...config.settings import settings

class PostgresConnection:
    """Gerenciador de conexão PostgreSQL"""

    _instance = None
    _engine = None
    _session_maker = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa a conexão"""
        self._engine = create_engine(settings.DATABASE_URL, echo=False)
        self._session_maker = sessionmaker(bind=self._engine)

    def get_session(self) -> SQLAlchemySession:
        """Retorna uma nova sessão"""
        return self._session_maker()

    @property
    def engine(self):
        """Retorna o engine SQLAlchemy"""
        return self._engine

postgres = PostgresConnection()
Session = postgres.get_session
