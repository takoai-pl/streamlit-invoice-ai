# Copyright (c) TaKo AI Sp. z o.o.

from src.data.models.business_table import BusinessTable
from src.data.models.client_table import ClientTable
from src.data.models.invoice_table import InvoiceTable
from src.data.models.product_table import ProductTable

business_table_mock = BusinessTable(
    name="Business",
    street="Street",
    postCode="12345",
    town="Town",
    country="Country",
    vatNo="123",
    bic="123",
    iban="123",
    phone="+123456",
    email="123",
)

business_table_mock_new = BusinessTable(
    name="Business New",
    street="Street New",
    postCode="54321",
    town="Town New",
    country="Country New",
    vatNo="321",
    bic="321",
    iban="321",
    phone="+654321",
    email="321",
)

business_table_mock_json = {
    "name": "Business",
    "street": "Street",
    "postCode": "12345",
    "town": "Town",
    "country": "Country",
    "vatNo": "123",
    "bic": "123",
    "iban": "123",
    "phone": "+123456",
    "email": "123",
}

client_table_mock = ClientTable(
    name="Client",
    street="Street",
    postCode="12345",
    town="Town",
    country="Country",
    vatNo="123",
)

client_table_mock_json = {
    "name": "Client",
    "street": "Street",
    "postCode": "12345",
    "town": "Town",
    "country": "Country",
    "vatNo": "123",
}

invoice_table_mock = InvoiceTable(
    invoiceNo="123",
    currency="USD",
    vatPercent=20,
    issuedAt="2022-01-01",
    dueTo="2022-02-01",
    note="Note",
    business_id=business_table_mock.businessID,
    client_id=client_table_mock.clientID,
    language="en",
)

product_table_mock = ProductTable(
    description="Product",
    quantity=1.0,
    unit="Unit",
    price=100.0,
    vatPercent=20.0,
    invoice_id=invoice_table_mock.invoiceId,
)
