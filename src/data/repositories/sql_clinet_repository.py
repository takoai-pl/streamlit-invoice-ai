# Copyright (c) TaKo AI Sp. z o.o.

from typing import Any, List

from src import ClientTable, DatabaseProvider
from src.domain import ClientEntity
from src.domain.repositories.client_repository_interface import (
    ClientRepositoryInterface,
)


class SQLClientRepository(ClientRepositoryInterface):
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "SQLClientRepository":
        if not cls._instance:
            cls._instance = super(SQLClientRepository, cls).__new__(cls)
        return cls._instance

    def __init__(self, database_provider: DatabaseProvider):
        self.database_provider = database_provider

    def get_all_clients(self) -> List[ClientEntity]:
        return [
            ClientEntity(**client.__dict__)
            for client in self.database_provider.client_list()
        ]

    def get_client_by_name(self, client_name: str) -> ClientEntity | None:
        client = self.database_provider.client_get(client_name)
        if not client:
            return None

        return ClientEntity(**client.__dict__)

    def create_client(self, client: ClientEntity) -> None:
        self.database_provider.client_add(ClientTable.from_model(client))

    def update_client(self, client: ClientEntity) -> None:
        self.database_provider.client_put(ClientTable.from_model(client))

    def delete_client(self, client_name: str) -> None:
        self.database_provider.client_del(client_name)
