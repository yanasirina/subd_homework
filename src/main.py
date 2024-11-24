import random

from db_workers import Atelier, AtelierData, Service, ServiceData, ServiceCostInAtelier, CostData
from db_connection import get_connection
from decimal import Decimal

if __name__ == '__main__':
    connection = get_connection()

    # создадим объекты для работы с таблицами
    atelier_worker = Atelier(connection)
    service_worker = Service(connection)
    cost_worker = ServiceCostInAtelier(connection)

    try:
        # предварительно очистим таблицы
        atelier_worker.clean_table()
        service_worker.clean_table()
        cost_worker.clean_table()

        # создадим ателье и проверим, что оно появилось в бд
        new_atelier = atelier_worker.create_atelier(
            AtelierData(name="Atelier A", address="123 Main St", phone_number="1234567890")
        )
        ateliers_in_db = atelier_worker.get_ateliers()
        assert len(ateliers_in_db) == 1
        assert ateliers_in_db[0].atelier_id == new_atelier.atelier_id

        # создадим несколько ателье и проверим, что они появились в бд
        multiple_ateliers = atelier_worker.create_ateliers([
            AtelierData(name="Atelier B", address="456 Elm St", phone_number="0987654321"),
            AtelierData(name="Atelier C", address="789 Oak St", phone_number="1112223333")
        ])
        ateliers_in_db = atelier_worker.get_ateliers()
        assert len(ateliers_in_db) == 3

        # обновим данные у ателье и проверим, что они изменились в бд
        updated_atelier = atelier_worker.update_atelier(
            new_atelier.atelier_id,
            AtelierData(name="Updated Atelier A", address="Updated 123 Main St", phone_number="1234509876")
        )
        atelier_from_db = atelier_worker.get_atelier_by_id(new_atelier.atelier_id)
        assert atelier_from_db.name == "Updated Atelier A"
        assert atelier_from_db.address == "Updated 123 Main St"
        assert atelier_from_db.phone_number == "1234509876"

        # проверим фильтрацию
        ateliers = atelier_worker.get_ateliers_by_name("Updated Atelier A")
        assert len(ateliers) == 1
        assert ateliers[0].name == "Updated Atelier A"
        ateliers = atelier_worker.get_ateliers_by_phone("1234509876")
        assert len(ateliers) == 1
        assert ateliers[0].phone_number == "1234509876"

        # создадим услугу и проверим, что она появилось в бд
        new_service = service_worker.create_service(ServiceData(name="Cleaning", execution_time=2))
        services_in_db = service_worker.get_services()
        assert len(services_in_db) == 1
        assert services_in_db[0].service_id == new_service.service_id

        # создадим несколько услуг и проверим, что они появились в бд
        multiple_services = service_worker.create_services([
            ServiceData(name="Repair", execution_time=5),
            ServiceData(name="Painting", execution_time=3)
        ])
        services_in_db = service_worker.get_services()
        assert len(services_in_db) == 3

        # обновим данные у услуги и проверим, что они изменились в бд
        updated_service = service_worker.update_service(
            new_service.service_id,
            ServiceData(name="Deep Cleaning", execution_time=3)
        )
        service_from_db = service_worker.get_service_by_id(new_service.service_id)
        assert service_from_db.name == "Deep Cleaning"
        assert service_from_db.execution_time == 3

        # проверим фильтрацию
        service = service_worker.get_service_by_name("Deep Cleaning")
        assert service.name == "Deep Cleaning"

        # проверим создание стоимостей
        for atelier in atelier_worker.get_ateliers():
            for service in service_worker.get_services():
                random_cost = Decimal(random.randrange(100, 1000))
                cost_worker.create_cost(
                    service_id=service.service_id,
                    atelier_id=atelier.atelier_id,
                    cost_data=CostData(cost=random_cost),
                )
        assert len(cost_worker.get_costs()) == 9

        # проверим обновление стоимости
        updated_cost = cost_worker.update_cost(
            service_id=new_service.service_id,
            atelier_id=new_atelier.atelier_id,
            cost_data=CostData(cost=Decimal("120.00"))
        )
        cost_from_db = cost_worker.get_cost(new_service.service_id, new_atelier.atelier_id)
        assert cost_from_db.cost == Decimal("120.00")

        # проверим удаление конкретных объектов
        cost_worker.delete_cost(new_service.service_id, new_atelier.atelier_id)
        assert len(cost_worker.get_costs()) == 8
        atelier_worker.delete_atelier(new_atelier.atelier_id)
        assert len(atelier_worker.get_ateliers()) == 2
        service_worker.delete_service(new_service.service_id)
        assert len(service_worker.get_services()) == 2

        # проверим очистку таблиц
        atelier_worker.clean_table()
        assert len(atelier_worker.get_ateliers()) == 0
        service_worker.clean_table()
        assert len(service_worker.get_services()) == 0
        cost_worker.clean_table()
        assert len(cost_worker.get_costs()) == 0

    finally:
        connection.close()
