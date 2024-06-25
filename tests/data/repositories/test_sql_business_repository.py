# Copyright (c) TaKo AI Sp. z o.o.

from src.data.models.business_table import BusinessTable
from src.data.providers.database_provider import DatabaseProvider
from src.data.repositories.sql_business_repository import SQLBusinessRepository
from src.domain.entities.business_entity import BusinessEntity

from tests.mocks.populate_database_mock import (
    erase_database,
    populate_database,
)
from tests.mocks.schema_mocks import business_table_mock


class TestSQLBusinessRepository(object):
    @classmethod
    def setup_class(cls) -> None:
        erase_database()

    def setup_method(self) -> None:
        db_url = populate_database()
        self.dataProvider = DatabaseProvider(db_url)
        self.repository = SQLBusinessRepository(self.dataProvider)

    @staticmethod
    def check_business(
        business: BusinessEntity, mock: BusinessEntity | BusinessTable
    ) -> None:
        assert isinstance(business, BusinessEntity) or isinstance(business, BusinessTable)
        assert business.name == mock.name
        assert business.street == mock.street
        assert business.postCode == mock.postCode
        assert business.town == mock.town
        assert business.country == mock.country
        assert business.vatNo == mock.vatNo
        assert business.iban == mock.iban
        assert business.phone == mock.phone
        assert business.email == mock.email

    def test_get_all_businesses(self) -> None:
        businesses = self.repository.get_all_businesses()
        assert len(businesses) == 1
        assert isinstance(businesses, list)
        self.check_business(businesses[0], business_table_mock)

    def test_get_all_businesses_empty(self, monkeypatch) -> None:
        monkeypatch.setattr(self.dataProvider, "business_list", lambda: [])
        businesses = self.repository.get_all_businesses()
        assert len(businesses) == 0

    def test_get_business(self) -> None:
        business = self.repository.get_business_by_name(str(business_table_mock.name))
        self.check_business(business, business_table_mock)

    def test_get_business_empty(self) -> None:
        business = self.repository.get_business_by_name("Not a business")
        assert business is None

    def test_add_business(self) -> None:
        model = BusinessTable.to_model(business_table_mock)
        model.name = "New Business"
        model.vatNo = "New VAT"
        model.bic = "New BIC"

        self.repository.create_business(model)
        business = self.repository.get_business_by_name(str(model.name))
        self.check_business(business, model)

    def test_change_business_details(self) -> None:
        business = self.repository.get_business_by_name(str(business_table_mock.name))
        self.check_business(business, business_table_mock)

        business.vatNo = "New VAT"
        business.email = "New Email"
        self.repository.update_business(business)

        new_business = self.repository.get_business_by_name(str(business.name))
        self.check_business(business, new_business)

    def test_delete_business(self) -> None:
        business = self.repository.get_business_by_name(str(business_table_mock.name))
        self.check_business(business, business_table_mock)

        self.repository.delete_business(str(business_table_mock.name))
        business = self.repository.get_business_by_name(str(business_table_mock.name))
        assert business is None
