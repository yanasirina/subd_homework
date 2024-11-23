from typing import NamedTuple
from entities import Atelier as AtelierEntity


class _AtelierData(NamedTuple):
    name: str
    address: str
    phone_number: str


class Service:
    def create_atelier(self, service_data: _AtelierData) -> AtelierEntity:
        ...

    def create_ateliers(self, service_data: list[_AtelierData]) -> list[AtelierEntity]:
        ...
