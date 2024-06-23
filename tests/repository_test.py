# Copyright (c) TaKo AI Sp. z o.o.
from typing import Any

import pytest

from src.data.providers.database_provider import DatabaseProvider
from src.data.repository import Repository
from src.domain.models import (
    Business,
    Client
)

from .mock_populate_database import populate_database
from .mocks.models_mocks import (
    business_model_mock
)

from .mocks.schema_mocks import (
    business_table_mock,
    client_table_mock,
    invoice_table_mock,
    product_table_mock
)


def check_business(business: Any, mock: Any) -> None:
    assert isinstance(business, Business)
    assert business.name == mock.name
    assert business.street == mock.street
    assert business.postCode == mock.postCode
    assert business.town == mock.town
    assert business.country == mock.country
    assert business.vatNo == mock.vatNo
    assert business.iban == mock.iban
    assert business.phone == mock.phone
    assert business.email == mock.email


def test_get_business() -> None:
    db_path = populate_database()
    dataProvider = DatabaseProvider(db_path)
    repository = Repository(dataProvider)
    business = repository.get_business(business_table_mock.name)

    check_business(business, business_table_mock)


def test_add_business() -> None:
    db_path = populate_database()
    dataProvider = DatabaseProvider(db_path)
    repository = Repository(dataProvider)

    repository.add_business(business_model_mock)
    if business_model_mock.name is None:
        raise ValueError("business_model_mock.name cannot be None")
    business = repository.get_business(business_model_mock.name)

    check_business(business, business_model_mock)


def test_get_client() -> None:
    db_path = populate_database()
    dataProvider = DatabaseProvider(db_path)
    repository = Repository(dataProvider)
    client = repository.get_client(client_table_mock.name)

    assert isinstance(client, Client)
    assert client.name == client_table_mock.name
    assert client.street == client_table_mock.street
    assert client.postCode == client_table_mock.postCode
    assert client.town == client_table_mock.town
    assert client.country == client_table_mock.country
    assert client.vatNo == client_table_mock.vatNo

