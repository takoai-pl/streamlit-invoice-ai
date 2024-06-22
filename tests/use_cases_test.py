# Copyright (c) TaKo AI Sp. z o.o.

import pytest

from .factories import BusinessFactory, ClientFactory, InvoiceFactory, ProductFactory
from src.infrastructure.providers.database_schema import session
from src.infrastructure.providers.database_provider import (
    get_business,
    get_all_products,
    get_invoice_by_client,
    get_product_by_invoice
)


def test_get_business():
    # Create a mock business
    mock_business = BusinessFactory.create()

    # Test the get_business function
    result = get_business(session, mock_business.id)
    assert result == mock_business


def test_get_all_products():
    # Create mock products
    mock_products = ProductFactory.create_batch(5)

    # Test the get_all_products function
    results = get_all_products(session)
    assert len(results) == len(mock_products)
    assert set(results) == set(mock_products)


def test_get_invoice_by_client():
    # Create a mock client and invoices
    mock_client = ClientFactory.create()
    mock_invoices = InvoiceFactory.create_batch(5, client_id=mock_client.id)

    # Test the get_invoice_by_client function
    results = get_invoice_by_client(session, mock_client.id)
    assert len(results) == len(mock_invoices)
    assert set(results) == set(mock_invoices)


def test_get_product_by_invoice():
    # Create a mock invoice and products
    mock_invoice = InvoiceFactory.create()
    mock_products = ProductFactory.create_batch(5, invoice_id=mock_invoice.id)

    # Test the get_product_by_invoice function
    results = get_product_by_invoice(session, mock_invoice.id)
    assert len(results) == len(mock_products)
    assert set(results) == set(mock_products)
