from typing import NamedTuple
from psycopg2.extensions import connection
from entities import Service as ServiceEntity


class _ServiceData(NamedTuple):
    name: str
    execution_time: int = None


class Service:
    def __init__(self, connection: connection):
        self.connection = connection

    def create_service(self, service_data: _ServiceData) -> ServiceEntity:
        ...

    def create_services(self, service_data: list[_ServiceData]) -> list[ServiceEntity]:
        ...

    def update_service(self, service_id: int, service_data: _ServiceData) -> ServiceEntity:
        ...

    def get_services(self, limit: int = None, offset: int = None) -> list[ServiceEntity]:
        ...

    def get_service_by_id(self, service_id: int) -> ServiceEntity:
        ...

    def get_service_by_name(self, service_id: int) -> ServiceEntity:
        ...

    def get_most_expensive_services(self, count: int) -> list[ServiceEntity]:
        ...

    def get_cheapest_services(self, count: int) -> list[ServiceEntity]:
        ...

    def delete_service(self, service_id: int) -> None:
        ...

    def clean_table(self) -> None:
        ...
