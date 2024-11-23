from typing import NamedTuple
from decimal import Decimal
from entities import ServiceCostInAtelier as CostEntity


class _CostData(NamedTuple):
    service_id: int
    atelier_id: int
    cost: Decimal


class Service:
    def create_atelier(self, service_data: _CostData) -> CostEntity:
        ...

    def create_ateliers(self, service_data: list[_CostData]) -> list[CostEntity]:
        ...
