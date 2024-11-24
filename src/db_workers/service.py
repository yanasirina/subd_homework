from typing import NamedTuple
from psycopg2.extensions import connection
from entities import Service as ServiceEntity


class ServiceData(NamedTuple):
    name: str
    execution_time: int = None


class Service:
    def __init__(self, connection: connection):
        self.connection = connection

    def create_service(self, service_data: ServiceData) -> ServiceEntity:
        query = """
        INSERT INTO service (name, execution_time)
        VALUES (%s, %s)
        RETURNING service_id, name, execution_time;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (service_data.name, service_data.execution_time))
            result = cursor.fetchone()
            self.connection.commit()
        return ServiceEntity(*result)

    def create_services(self, service_data: list[ServiceData]) -> list[ServiceEntity]:
        query = """
        INSERT INTO service (name, execution_time)
        VALUES (%s, %s)
        RETURNING service_id, name, execution_time;
        """
        with self.connection.cursor() as cursor:
            results = []
            for data in service_data:
                cursor.execute(query, (data.name, data.execution_time))
                results.append(cursor.fetchone())  # Получаем результат для каждой вставленной записи
            self.connection.commit()
        return [ServiceEntity(*row) for row in results]

    def update_service(self, service_id: int, service_data: ServiceData) -> ServiceEntity:
        query = """
        UPDATE service
        SET name = %s, execution_time = %s
        WHERE service_id = %s
        RETURNING service_id, name, execution_time;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (service_data.name, service_data.execution_time, service_id))
            result = cursor.fetchone()
            self.connection.commit()
        return ServiceEntity(*result)

    def get_services(self) -> list[ServiceEntity]:
        query = "SELECT service_id, name, execution_time FROM service"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return [ServiceEntity(*row) for row in results]

    def get_service_by_id(self, service_id: int) -> ServiceEntity:
        query = "SELECT service_id, name, execution_time FROM service WHERE service_id = %s;"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (service_id,))
            result = cursor.fetchone()
        return ServiceEntity(*result) if result else None

    def get_service_by_name(self, name: str) -> ServiceEntity:
        query = "SELECT service_id, name, execution_time FROM service WHERE name = %s;"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (name,))
            result = cursor.fetchone()
        return ServiceEntity(*result) if result else None

    def delete_service(self, service_id: int) -> None:
        query = "DELETE FROM service WHERE service_id = %s;"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (service_id,))
            self.connection.commit()

    def clean_table(self) -> None:
        query = "DELETE FROM service;"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()
