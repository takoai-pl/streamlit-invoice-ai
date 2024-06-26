# Copyright (c) TaKo AI Sp. z o.o.
from src.domain.entities.client_entity import ClientEntity
from src.domain.repositories.client_repository_interface import (
    ClientRepositoryInterface,
)


class GetAllClientsNamesUseCase:
    def __init__(self, client_repository: ClientRepositoryInterface):
        self.client_repository = client_repository

    def execute(self) -> list[str | None]:
        response = self.client_repository.get_all_clients()
        return [client.name for client in response]


class GetClientDetailsUseCase:
    def __init__(self, client_repository: ClientRepositoryInterface) -> None:
        self.client_repository = client_repository

    def execute(self, client_name: str) -> ClientEntity | None:
        return self.client_repository.get_client_by_name(client_name)
