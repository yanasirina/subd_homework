from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Service:
    service_id: int
    name: str
    execution_time: int = None  # длительность выполнения в часах


@dataclass
class Atelier:
    atelier_id: int
    name: str
    address: str
    phone_number: str


@dataclass
class ServiceCostInAtelier:
    service: Service
    atelier: Atelier
    cost: Decimal
