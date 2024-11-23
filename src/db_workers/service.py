from typing import NamedTuple
from entities import Service as ServiceEntity


class _ServiceData(NamedTuple):
    name: str
    execution_time: int = None


class Service:
    def create_service(self, service_data: _ServiceData) -> ServiceEntity:
        ...

    def create_services(self, service_data: list[_ServiceData]) -> list[ServiceEntity]:
        ...
