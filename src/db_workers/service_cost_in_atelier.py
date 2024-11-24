from typing import NamedTuple
from decimal import Decimal
from psycopg2.extensions import connection
from entities import ServiceCostInAtelier as CostEntity


class CostData(NamedTuple):
    cost: Decimal


class ServiceCostInAtelier:
    def __init__(self, connection: connection):
        self.connection = connection

    def create_cost(self, service_id: int, atelier_id: int, cost_data: CostData) -> CostEntity:
        query = """
        INSERT INTO service_cost_in_atelier (service_id, atelier_id, cost)
        VALUES (%s, %s, %s)
        RETURNING service_id, atelier_id, cost;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (service_id, atelier_id, cost_data.cost))
            result = cursor.fetchone()
            self.connection.commit()
        return CostEntity(*result)

    def update_cost(self, service_id: int, atelier_id: int, cost_data: CostData) -> CostEntity:
        query = """
        UPDATE service_cost_in_atelier
        SET cost = %s
        WHERE service_id = %s AND atelier_id = %s
        RETURNING service_id, atelier_id, cost;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (cost_data.cost, service_id, atelier_id))
            result = cursor.fetchone()
            self.connection.commit()
        return CostEntity(*result)

    def get_cost(self, service_id: int, atelier_id: int) -> CostEntity:
        query = """
        SELECT service_id, atelier_id, cost
        FROM service_cost_in_atelier
        WHERE service_id = %s AND atelier_id = %s;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (service_id, atelier_id))
            result = cursor.fetchone()
        return CostEntity(*result)

    def get_costs(self) -> list[CostEntity]:
        query = "SELECT service_id, atelier_id, cost FROM service_cost_in_atelier"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return [CostEntity(*row) for row in results]

    def delete_cost(self, service_id: int, atelier_id: int) -> None:
        query = "DELETE FROM service_cost_in_atelier WHERE service_id = %s AND atelier_id = %s;"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (service_id, atelier_id))
            self.connection.commit()

    def clean_table(self) -> None:
        query = "DELETE FROM service_cost_in_atelier;"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()
