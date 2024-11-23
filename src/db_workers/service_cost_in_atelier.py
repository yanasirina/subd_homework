from typing import NamedTuple
from decimal import Decimal
from entities import ServiceCostInAtelier as CostEntity


class _CostData(NamedTuple):
    cost: Decimal


class ServiceCostInAtelier:
    def create_cost(self, service_id: int, atelier_id: int, service_data: _CostData) -> CostEntity:
        ...

    def update_cost(self, service_id: int, atelier_id: int, service_data: _CostData) -> CostEntity:
        ...

    def get_all_costs(self) -> list[CostEntity]:
        ...

    def delete_cost(self, service_id: int, atelier_id: int) -> None:
        ...

    def clean_table(self) -> None:
        ...
