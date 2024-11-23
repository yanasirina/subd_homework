from typing import NamedTuple
from entities import Atelier as AtelierEntity


class _AtelierData(NamedTuple):
    name: str
    address: str
    phone_number: str


class Atelier:
    def create_atelier(self, service_data: _AtelierData) -> AtelierEntity:
        ...

    def create_ateliers(self, service_data: list[_AtelierData]) -> list[AtelierEntity]:
        ...

    def update_atelier(self, atelier_id: int, atelier_data: _AtelierData) -> AtelierEntity:
        ...

    def get_all_ateliers(self) -> list[AtelierEntity]:
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
