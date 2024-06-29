# Copyright (c) TaKo AI Sp. z o.o.

from typing import Any, List

from frontend.data.models import BusinessModel
from frontend.data.providers.api_provider import APIProvider
from frontend.domain import BusinessEntity
from frontend.domain.repositories.business_repository_interface import (
    BusinessRepositoryInterface,
)


class APIBusinessRepository(BusinessRepositoryInterface):
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "APIBusinessRepository":
        if not cls._instance:
            cls._instance = super(APIBusinessRepository, cls).__new__(cls)
        return cls._instance

    def __init__(self, api_provider: APIProvider):
        self.database_provider = api_provider

    def get_all_businesses(self) -> List[BusinessEntity]:
        return [
            BusinessModel(**business.__dict__)
            for business in self.database_provider.business_list()
        ]

    def get_business_by_name(self, business_name: str) -> BusinessEntity | None:
        business = self.database_provider.business_get(business_name)
        if not business:
            return None

        return BusinessModel(**business.__dict__)

    def create_business(self, business: BusinessEntity) -> None:
        business = BusinessModel(**business.__dict__)
        self.database_provider.business_add(business)

    def update_business(self, business: BusinessEntity) -> None:
        business = BusinessModel(**business.__dict__)
        self.database_provider.business_put(business)

    def delete_business(self, business_name: str) -> None:
        self.database_provider.business_del(business_name)
