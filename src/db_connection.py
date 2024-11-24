import psycopg2
from psycopg2.extensions import connection
import config


class _DDL:
    def __init__(self, connection: connection):
        self.connection = connection

    def _create_service_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS service (
            service_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            execution_time INT DEFAULT NULL
        );
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def _create_atelier_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS atelier (
            atelier_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            address TEXT NOT NULL,
            phone_number VARCHAR(20) NOT NULL
        );
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def _create_service_cost_in_atelier_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS service_cost_in_atelier (
            service_id INT NOT NULL,
            atelier_id INT NOT NULL,
            cost NUMERIC(10, 2) NOT NULL,
            PRIMARY KEY (service_id, atelier_id),
            FOREIGN KEY (service_id) REFERENCES service(service_id) ON DELETE CASCADE,
            FOREIGN KEY (atelier_id) REFERENCES atelier(atelier_id) ON DELETE CASCADE
        );
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def create_tables(self):
        self._create_service_table()
        self._create_atelier_table()
        self._create_service_cost_in_atelier_table()


class _DatabaseConnector:
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
            self._connection = None


def get_connection() -> connection:
    return _DatabaseConnector().connection


def create_tables() -> None:
    connection = get_connection()
    _DDL(connection).create_tables()


if __name__ == '__main__':
    create_tables()
