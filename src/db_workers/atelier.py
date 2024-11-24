from typing import NamedTuple
from psycopg2.extensions import connection
from entities import Atelier as AtelierEntity


class AtelierData(NamedTuple):
    name: str
    address: str
    phone_number: str


class Atelier:
    def __init__(self, connection: connection):
        self.connection = connection

    def create_atelier(self, atelier_data: AtelierData) -> AtelierEntity:
        query = """
        INSERT INTO atelier (name, address, phone_number)
        VALUES (%s, %s, %s)
        RETURNING atelier_id, name, address, phone_number;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (atelier_data.name, atelier_data.address, atelier_data.phone_number))
            result = cursor.fetchone()
            self.connection.commit()
        return AtelierEntity(*result)

    def create_ateliers(self, atelier_data: list[AtelierData]) -> list[AtelierEntity]:
        query = """
        INSERT INTO atelier (name, address, phone_number)
        VALUES (%s, %s, %s)
        RETURNING atelier_id, name, address, phone_number;
        """
        with self.connection.cursor() as cursor:
            results = []
            for data in atelier_data:
                cursor.execute(query, (data.name, data.address, data.phone_number))
                results.append(cursor.fetchone())  # Получаем результат для каждой вставленной записи
            self.connection.commit()
        return [AtelierEntity(*row) for row in results]

    def update_atelier(self, atelier_id: int, atelier_data: AtelierData) -> AtelierEntity:
        query = """
        UPDATE atelier
        SET name = %s, address = %s, phone_number = %s
        WHERE atelier_id = %s
        RETURNING atelier_id, name, address, phone_number;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (atelier_data.name, atelier_data.address, atelier_data.phone_number, atelier_id))
            result = cursor.fetchone()
            self.connection.commit()
        return AtelierEntity(*result)

    def get_ateliers(self) -> list[AtelierEntity]:
        query = "SELECT atelier_id, name, address, phone_number FROM atelier"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return [AtelierEntity(*row) for row in results]

    def get_atelier_by_id(self, atelier_id: int) -> AtelierEntity:
        query = "SELECT atelier_id, name, address, phone_number FROM atelier WHERE atelier_id = %s;"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (atelier_id,))
            result = cursor.fetchone()
        return AtelierEntity(*result) if result else None

    def get_ateliers_by_name(self, name: str) -> list[AtelierEntity]:
        query = "SELECT atelier_id, name, address, phone_number FROM atelier WHERE name = %s;"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (name,))
            results = cursor.fetchall()
        return [AtelierEntity(*row) for row in results]

    def get_ateliers_by_phone(self, phone: str) -> list[AtelierEntity]:
        query = "SELECT atelier_id, name, address, phone_number FROM atelier WHERE phone_number = %s;"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (phone,))
            results = cursor.fetchall()
        return [AtelierEntity(*row) for row in results]

    def delete_atelier(self, atelier_id: int) -> None:
        query = "DELETE FROM atelier WHERE atelier_id = %s;"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (atelier_id,))
            self.connection.commit()

    def clean_table(self) -> None:
        query = "DELETE FROM atelier;"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()
