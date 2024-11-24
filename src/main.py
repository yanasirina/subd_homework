from db_workers import Atelier, Service, ServiceCostInAtelier
from db_connection import get_connection


if __name__ == '__main__':
    connection = get_connection()
    atelier = Atelier(connection)
    service = Service(connection)
    cost = ServiceCostInAtelier(connection)
