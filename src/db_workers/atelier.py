from typing import NamedTuple
from psycopg2.extensions import connection
from entities import Atelier as AtelierEntity


class _AtelierData(NamedTuple):
    name: str
    address: str
    phone_number: str


class Atelier:
    def __init__(self, connection: connection):
        self.connection = connection

    def create_atelier(self, service_data: _AtelierData) -> AtelierEntity:
        ...

    def create_ateliers(self, service_data: list[_AtelierData]) -> list[AtelierEntity]:
        ...

    def update_atelier(self, atelier_id: int, atelier_data: _AtelierData) -> AtelierEntity:
        ...

    def get_ateliers(self, limit: int = None, offset: int = None) -> list[AtelierEntity]:
        ...

    def get_atelier_by_id(self, service_id: int) -> AtelierEntity:
        ...

    def get_ateliers_by_name(self, service_id: int) -> list[AtelierEntity]:
        ...

    def get_ateliers_by_phone(self, service_id: int) -> list[AtelierEntity]:
        ...

    def delete_atelier(self, atelier_id: int) -> None:
        ...

    def clean_table(self) -> None:
        ...
