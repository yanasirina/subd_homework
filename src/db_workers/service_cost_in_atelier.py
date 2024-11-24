from typing import NamedTuple
from decimal import Decimal
from psycopg2.extensions import connection
from entities import ServiceCostInAtelier as CostEntity


class _CostData(NamedTuple):
    cost: Decimal


class ServiceCostInAtelier:
    def __init__(self, connection: connection):
        self.connection = connection

    def create_cost(self, service_id: int, atelier_id: int, cost_data: _CostData) -> CostEntity:
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

    def update_cost(self, service_id: int, atelier_id: int, cost_data: _CostData) -> CostEntity:
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

    def get_costs(self, limit: int = None, offset: int = None) -> list[CostEntity]:
        query = "SELECT service_id, atelier_id, cost FROM service_cost_in_atelier"
        if limit is not None:
            query += " LIMIT %s"
        if offset is not None:
            query += " OFFSET %s"

        with self.connection.cursor() as cursor:
            cursor.execute(query, (limit, offset) if limit and offset else ())
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
