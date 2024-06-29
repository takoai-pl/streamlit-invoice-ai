# Copyright (c) TaKo AI Sp. z o.o.

import pytest

from frontend.data.models.business_table import BusinessTable
from frontend.data.providers.database_provider import DatabaseProvider
from frontend.data.repositories.sql_business_repository import SQLBusinessRepository
from frontend.domain.entities.business_entity import BusinessEntity
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
        business: BusinessEntity | None, mock: BusinessEntity | BusinessTable
    ) -> None:
        assert isinstance(business, BusinessEntity | None) or isinstance(
            business, BusinessTable
        )
        assert business.name == mock.name  # type: ignore[union-attr]
        assert business.street == mock.street  # type: ignore[union-attr]
        assert business.postCode == mock.postCode  # type: ignore[union-attr]
        assert business.town == mock.town  # type: ignore[union-attr]
        assert business.country == mock.country  # type: ignore[union-attr]
        assert business.vatNo == mock.vatNo  # type: ignore[union-attr]
        assert business.iban == mock.iban  # type: ignore[union-attr]
        assert business.phone == mock.phone  # type: ignore[union-attr]
        assert business.email == mock.email  # type: ignore[union-attr]

    def test_get_all_businesses(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            self.dataProvider, "business_list", lambda: [business_table_mock]
        )
        businesses = self.repository.get_all_businesses()
        assert len(businesses) == 1
        assert isinstance(businesses, list)
        self.check_business(businesses[0], business_table_mock)

    def test_get_all_businesses_empty(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(self.dataProvider, "business_list", lambda: [])
        businesses = self.repository.get_all_businesses()
        assert len(businesses) == 0

    def test_get_business(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            self.dataProvider, "business_get", lambda x: business_table_mock
        )
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

    def test_delete_business(self, monkeypatch: pytest.MonkeyPatch) -> None:
        business_table_mock.name = "New Business"  # type: ignore[assignment]
        self.repository.delete_business(str(business_table_mock.name))
        business = self.repository.get_business_by_name(str(business_table_mock.name))
        assert business is None
