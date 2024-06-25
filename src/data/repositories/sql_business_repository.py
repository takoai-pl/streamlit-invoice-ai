from typing import Any

from src.data.providers.database_provider import DatabaseProvider
from src.domain.repositories.business_repository_interface import BusinessRepositoryInterface
from src.data.models.business_table import BusinessTable
from src.domain.entities.business_entity import BusinessEntity


class SQLBusinessRepository(BusinessRepositoryInterface):
    """SQL implementation of the BusinessRepositoryInterface. Singleton class."""

    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "SQLBusinessRepository":
        if not cls._instance:
            cls._instance = super(SQLBusinessRepository, cls).__new__(cls)
        return cls._instance

    def __init__(self, database_provider: DatabaseProvider):
        """
        Initialize the SQLBusinessRepository.
        :param database_provider:
        """
        self.database_provider = database_provider

    def get_all_businesses(self) -> list[BusinessEntity]:
        """
        Get all businesses from the database.

        :return: List of BusinessEntity objects
        """
        return [
                BusinessEntity(**business.__dict__)
                for business in self.database_provider.business_list()
            ]

    def get_business_by_name(self, business_name: str) -> BusinessEntity | None:
        """
        Get a business by its name.
        :param business_name: name of the business to get
        :return: BusinessEntity object
        """
        business = self.database_provider.business_get(business_name)
        if not business:
            return None

        return BusinessEntity(**business.__dict__)

    def create_business(self, business: BusinessEntity) -> None:
        """
        Create a new business.
        :param business:
        """
        self.database_provider.business_add(BusinessTable.from_model(business))

    def update_business(self, business: BusinessEntity) -> None:
        """
        Update a business.
        :param business: new BusinessEntity object to replace the old one
        """
        self.database_provider.business_put(BusinessTable.from_model(business))

    def delete_business(self, business_name: str) -> None:
        """
        Delete a business.
        :param business_name: name of the business to delete
        """
        self.database_provider.business_del(business_name)
