# Copyright (c) TaKo AI Sp. z o.o.

from typing import Any

from src.data.models.business_table import BusinessTable
from src.data.providers.database_provider import DatabaseProvider
from src.domain.entities.business_entity import BusinessEntity
from src.domain.entities.client_entity import ClientEntity


class Repository:
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "Repository":
        if not cls._instance:
            cls._instance = super(Repository, cls).__new__(cls)
        return cls._instance

    def __init__(self, database_provider: DatabaseProvider) -> None:
        self.database_provider = database_provider

    def get_business(self, business_name: str) -> BusinessEntity:
        return BusinessEntity(
            **self.database_provider.get_business(business_name).__dict__
        )

    def change_business_details(self, business: BusinessEntity) -> None:
        self.database_provider.change_business_details(business)

    def add_business(self, business: BusinessEntity) -> None:
        business_table = BusinessTable.from_model(business)
        self.database_provider.add_business(business_table)

    def get_client(self, client_name: str) -> ClientEntity:
        return ClientEntity(**self.database_provider.get_client(client_name).__dict__)
