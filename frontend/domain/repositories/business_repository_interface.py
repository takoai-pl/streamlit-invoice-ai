# Copyright (c) TaKo AI Sp. z o.o.

from abc import ABC, abstractmethod
from typing import List

from frontend.domain import BusinessEntity


class BusinessRepositoryInterface(ABC):
    @abstractmethod
    def get_all_businesses(self) -> List[BusinessEntity]:
        pass

    @abstractmethod
    def get_business_by_id(self, business_id: str) -> BusinessEntity | None:
        pass

    @abstractmethod
    def create_business(self, business: BusinessEntity) -> None:
        pass

    @abstractmethod
    def update_business(self, business: BusinessEntity) -> None:
        pass

    @abstractmethod
    def delete_business(self, business_id: str) -> None:
        pass
