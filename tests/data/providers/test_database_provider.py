# Copyright (c) TaKo AI Sp. z o.o.

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.data.providers.database_provider import (
    BusinessAlreadyExistsException,
    BusinessNotFoundException,
    BusinessRetrievalException,
    DatabaseConnectionException,
    DatabaseProvider,
)

from tests.mocks.populate_database_mock import (
    erase_database,
    populate_database,
)
from tests.mocks.schema_mocks import business_table_mock


class TestDatabaseProviderBusiness(object):
    @classmethod
    def setup_class(cls) -> None:
        erase_database()

    def setup_method(self) -> None:
        db_url = populate_database()
        self.dataProvider = DatabaseProvider(db_url)

    def test_database_connection_exception(self) -> None:
        with pytest.raises(DatabaseConnectionException):
            DatabaseProvider("sqlite:/$$$")

    def test_business_list(self) -> None:
        businesses = self.dataProvider.business_list()
        assert len(businesses) == 1
        assert isinstance(businesses, list)

    def test_business_list_exception(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def mock_query() -> None:
            raise SQLAlchemyError("Mocked SQLAlchemy error")

        monkeypatch.setattr(Session, "query", mock_query)
        with pytest.raises(BusinessRetrievalException) as excinfo:
            self.dataProvider.business_list()

        assert "Could not retrieve businesses" in str(excinfo.value)

    def test_business_get(self) -> None:
        business = self.dataProvider.business_get("Business")
        assert business is not None

    def test_business_get_none(self, monkeypatch: pytest.MonkeyPatch) -> None:
        business = self.dataProvider.business_get("Not a business")
        assert business is None

    def test_business_get_exception(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def mock_query() -> None:
            raise SQLAlchemyError("Mocked SQLAlchemy error")

        monkeypatch.setattr(Session, "query", mock_query)
        with pytest.raises(BusinessRetrievalException) as excinfo:
            self.dataProvider.business_get("Test Business")

        assert "Could not retrieve business" in str(excinfo.value)

    def test_business_add_already_exists(self) -> None:
        with pytest.raises(BusinessAlreadyExistsException) as excinfo:
            self.dataProvider.business_add(business_table_mock)

        assert (
            f"Business with name '{business_table_mock.name}' already exists."
            in str(excinfo.value)
        )

    def test_business_add(self) -> None:
        business_table_mock.name = "New Business"  # type: ignore[assignment]

        self.dataProvider.business_add(business_table_mock)  # type: ignore[arg-type]
        business = self.dataProvider.business_get(business_table_mock.name)
        assert business is not None
        assert business.name == business_table_mock.name

    def test_business_put(self) -> None:
        business_table_mock.iban = "New IBAN"  # type: ignore[assignment]
        business_table_mock.email = "New EMAIL"  # type: ignore[assignment]
        self.dataProvider.business_put(business_table_mock)
        business = self.dataProvider.business_get(business_table_mock.name)
        assert business is not None
        assert business.iban == "New IBAN"  # type: ignore[assignment]
        assert business.email == "New EMAIL"  # type: ignore[assignment]

    def test_business_put_no_business(self) -> None:
        business_table_mock.name = "Not a business"  # type: ignore[assignment]
        with pytest.raises(BusinessNotFoundException) as excinfo:
            self.dataProvider.business_put(business_table_mock)

        assert f"No business found with name {business_table_mock.name}" in str(
            excinfo.value
        )

    def test_business_put_name_change(self) -> None:
        business_table_mock.name = "New Business Name"  # type: ignore[assignment]
        with pytest.raises(BusinessNotFoundException) as excinfo:
            self.dataProvider.business_put(business_table_mock)

        assert "No business found with name" in str(excinfo.value)

    def test_business_del(self) -> None:
        self.dataProvider.business_del(business_table_mock.name)
        business = self.dataProvider.business_get(business_table_mock.name)
        assert business is None

        self.dataProvider.business_add(business_table_mock)

    def test_business_del_no_business(self) -> None:
        with pytest.raises(BusinessNotFoundException) as excinfo:
            self.dataProvider.business_del("Not a business")

        assert "No business found with name" in str(excinfo.value)
