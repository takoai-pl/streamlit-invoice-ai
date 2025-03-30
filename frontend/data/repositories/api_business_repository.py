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
        businesses = [
            BusinessModel(**business.__dict__)
            for business in self.database_provider.business_list()
        ]

        # Filter businesses based on user access
        if hasattr(self.database_provider, "user") and self.database_provider.user:
            user_business_ids = self.database_provider.user.get("business_ids", [])
            businesses = [
                business
                for business in businesses
                if business.businessID in user_business_ids
            ]

        return businesses

    def get_business_by_id(self, business_id: str) -> BusinessEntity | None:
        # Check if user has access to this business
        if hasattr(self.database_provider, "user") and self.database_provider.user:
            user_business_ids = self.database_provider.user.get("business_ids", [])
            if business_id not in user_business_ids:
                return None

        business = self.database_provider.business_get(business_id)
        if not business:
            return None

        return BusinessModel(**business.__dict__)

    def create_business(self, business: BusinessEntity) -> None:
        business = BusinessModel(**business.__dict__)
        self.database_provider.business_add(business)

    def update_business(self, business: BusinessEntity) -> None:
        # Check if user has access to this business
        if hasattr(self.database_provider, "user") and self.database_provider.user:
            user_business_ids = self.database_provider.user.get("business_ids", [])
            if business.businessID not in user_business_ids:
                return

        business = BusinessModel(**business.__dict__)
        self.database_provider.business_put(business)

    def delete_business(self, business_id: str) -> None:
        # Check if user has access to this business
        if hasattr(self.database_provider, "user") and self.database_provider.user:
            user_business_ids = self.database_provider.user.get("business_ids", [])
            if business_id not in user_business_ids:
                return

        self.database_provider.business_del(business_id)
