# Copyright (c) TaKo AI Sp. z o.o.

from typing import Any

from src.data.providers.database_provider import DatabaseProvider
from src.data.providers.database_schema import (
    BusinessTable,
)
from src.domain.models import (
    Invoice,
    Product,
    Business,
    Client,
)


class Repository:
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "Repository":
        if not cls._instance:
            cls._instance = super(Repository, cls).__new__(cls)
        return cls._instance

    def __init__(self, database_provider: DatabaseProvider) -> None:
        self.database_provider = database_provider

    def get_business(self, business_name: str) -> Business:
        return Business(**self.database_provider.get_business(business_name).__dict__)

    def change_business_details(self, business: Business) -> None:
        self.database_provider.change_business_details(business)

    def add_business(self, business: Business) -> None:
        business_table = BusinessTable.from_model(business)
        self.database_provider.add_business(business_table)

    def get_client(self, client_name: str) -> Client:
        return Client(**self.database_provider.get_client(client_name).__dict__)
