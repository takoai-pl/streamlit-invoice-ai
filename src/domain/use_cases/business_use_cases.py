# Copyright (c) TaKo AI Sp. z o.o.

from src.domain import BusinessEntity
from src.domain.repositories.business_repository_interface import (
    BusinessRepositoryInterface,
)


class GetBusinessDetailsUseCase:
    def __init__(self, business_repository: BusinessRepositoryInterface):
        self.business_repository = business_repository

    def execute(self, business_name: str) -> BusinessEntity | None:
        return self.business_repository.get_business_by_name(business_name)


class GetAllBusinessesNamesUseCase:
    def __init__(self, business_repository: BusinessRepositoryInterface):
        self.business_repository = business_repository

    def execute(self) -> list[str | None]:
        response = self.business_repository.get_all_businesses()
        return [business.name for business in response]


class EditBusinessUseCase:
    def __init__(self, business_repository: BusinessRepositoryInterface):
        self.business_repository = business_repository

    def execute(self, business: BusinessEntity) -> BusinessEntity | None:
        return self.business_repository.update_business(business)


class CreateBusinessUseCase:
    def __init__(self, business_repository: BusinessRepositoryInterface):
        self.business_repository = business_repository

    def execute(self, business: BusinessEntity) -> BusinessEntity | None:
        return self.business_repository.create_business(business)


class DeleteBusinessUseCase:
    def __init__(self, business_repository: BusinessRepositoryInterface):
        self.business_repository = business_repository

    def execute(self, business_name: str) -> BusinessEntity | None:
        return self.business_repository.delete_business(business_name)
