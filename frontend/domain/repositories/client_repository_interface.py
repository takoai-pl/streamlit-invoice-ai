# Copyright (c) TaKo AI Sp. z o.o.

from abc import ABC, abstractmethod
from typing import List

from frontend.domain import ClientEntity


class ClientRepositoryInterface(ABC):
    @abstractmethod
    def get_all_clients(self) -> List[ClientEntity]:
        pass

    @abstractmethod
    def get_client_by_id(self, client_id: str) -> ClientEntity | None:
        pass

    @abstractmethod
    def create_client(self, client: ClientEntity) -> None:
        pass

    @abstractmethod
    def update_client(self, client: ClientEntity) -> None:
        pass

    @abstractmethod
    def delete_client(self, client_id: str) -> None:
        pass
