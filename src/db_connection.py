import psycopg2
from psycopg2.extensions import connection
import config


class DatabaseConnection:
    """Класс для реализации Singleton подключения к PostgreSQL."""
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._connection = cls._create_connection()
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
            print("Соединение с базой данных закрыто.")
            self._connection = None
