from typing import NamedTuple
from decimal import Decimal
from psycopg2.extensions import connection
from entities import ServiceCostInAtelier as CostEntity


class _CostData(NamedTuple):
    cost: Decimal


class ServiceCostInAtelier:
    def __init__(self, connection: connection):
        self.connection = connection

    def create_cost(self, service_id: int, atelier_id: int, service_data: _CostData) -> CostEntity:
        ...

    def update_cost(self, service_id: int, atelier_id: int, service_data: _CostData) -> CostEntity:
        ...

    def get_costs(self, limit: int = None, offset: int = None) -> list[CostEntity]:
        ...

    def delete_cost(self, service_id: int, atelier_id: int) -> None:
        ...

    def clean_table(self) -> None:
        ...
