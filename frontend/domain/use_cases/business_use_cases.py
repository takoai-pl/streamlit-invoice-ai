# Copyright (c) TaKo AI Sp. z o.o.
from frontend.domain import BusinessEntity
from frontend.domain.repositories.business_repository_interface import (
    BusinessRepositoryInterface,
)


class GetBusinessDetailsUseCase:
    def __init__(self, business_repository: BusinessRepositoryInterface):
        self.business_repository = business_repository

    def execute(self, business_id: str) -> BusinessEntity | None:
        return self.business_repository.get_business_by_id(business_id)


class GetAllBusinessesUseCase:
    def __init__(self, business_repository: BusinessRepositoryInterface):
        self.business_repository = business_repository

    def execute(self) -> list[BusinessEntity]:
        return self.business_repository.get_all_businesses()


class UpdateBusinessUseCase:
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
