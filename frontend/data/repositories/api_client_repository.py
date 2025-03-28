# Copyright (c) TaKo AI Sp. z o.o.
from abc import ABC
from typing import Any, List

from frontend.data.models import ClientModel
from frontend.data.providers import APIProvider
from frontend.domain import ClientEntity
from frontend.domain.repositories.client_repository_interface import (
    ClientRepositoryInterface,
)


class APIClientRepository(ClientRepositoryInterface, ABC):
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "APIClientRepository":
        if not cls._instance:
            cls._instance = super(APIClientRepository, cls).__new__(cls)
        return cls._instance

    def __init__(self, api_provider: APIProvider):
        self.database_provider = api_provider

    def get_all_clients(self) -> List[ClientEntity]:
        return [
            ClientEntity(**client.__dict__)
            for client in self.database_provider.client_list()
        ]

    def get_client_by_id(self, client_id: str) -> ClientEntity | None:
        client = self.database_provider.client_get(client_id)
        if not client:
            return None

        return ClientEntity(**client.__dict__)

    def create_client(self, client: ClientEntity) -> None:
        client = ClientModel(**client.__dict__)
        self.database_provider.client_add(client)

    def update_client(self, client: ClientEntity) -> None:
        client = ClientModel(**client.__dict__)
        self.database_provider.client_put(client)

    def delete_client(self, client_id: str) -> None:
        self.database_provider.client_del(client_id)
