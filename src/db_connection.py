import psycopg2
from psycopg2.extensions import connection
import config


class _DDL:
    def __init__(self):
        self.connection = DatabaseConnector().connection

    def _create_service_table(self):
        pass

    def _create_atelier_table(self):
        pass

    def _create_service_cost_in_atelier_table(self):
        pass

    def create_tables(self):
        self._create_service_table()
        self._create_atelier_table()
        self._create_service_cost_in_atelier_table()


class DatabaseConnector:
    """Класс для реализации Singleton подключения к PostgreSQL."""
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._connection = cls._create_connection()
            _DDL().create_tables()
        return cls._instance

    @staticmethod
    def _create_connection() -> connection:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
        )
        return conn

    @property
    def connection(self) -> connection:
        return self._connection

    def close(self) -> None:
        if self._connection:
            self._connection.close()
            self._connection = None
