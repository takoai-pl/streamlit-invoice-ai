# Copyright (c) TaKo AI Sp. z o.o.

from src.data.models.business_table import BusinessTable
from src.data.providers.database_provider import DatabaseProvider
from src.data.repositories.repository import Repository
from src.domain.entities.business_entity import BusinessEntity
from src.domain.entities.client_entity import ClientEntity

from .mock_populate_database import (
    erase_database,
    populate_database,
)
from .mocks.models_mocks import business_model_mock
from .mocks.schema_mocks import business_table_mock, client_table_mock


class TestRepository(object):
    @classmethod
    def setup_class(cls) -> None:
        erase_database()

    def setup_method(self) -> None:
        self.db_path = populate_database()
        self.dataProvider = DatabaseProvider(self.db_path)
        self.repository = Repository(self.dataProvider)

    @staticmethod
    def check_business(
        business: BusinessEntity, mock: BusinessEntity | BusinessTable
    ) -> None:
        assert isinstance(business, BusinessEntity)
        assert business.name == mock.name
        assert business.street == mock.street
        assert business.postCode == mock.postCode
        assert business.town == mock.town
        assert business.country == mock.country
        assert business.vatNo == mock.vatNo
        assert business.iban == mock.iban
        assert business.phone == mock.phone
        assert business.email == mock.email

    def test_get_client(self) -> None:
        client = self.repository.get_client(str(client_table_mock.name))

        assert isinstance(client, ClientEntity)
        assert client.name == client_table_mock.name
        assert client.street == client_table_mock.street
        assert client.postCode == client_table_mock.postCode
        assert client.town == client_table_mock.town
        assert client.country == client_table_mock.country
        assert client.vatNo == client_table_mock.vatNo

    def test_get_business(self) -> None:
        business = self.repository.get_business(str(business_table_mock.name))
        self.check_business(business, business_table_mock)

    def test_add_business(self) -> None:
        self.repository.add_business(business_model_mock)
        if business_model_mock.name is None:
            raise ValueError("business_model_mock.name cannot be None")
        business = self.repository.get_business(str(business_model_mock.name))
        self.check_business(business, business_model_mock)
