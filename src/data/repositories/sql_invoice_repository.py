# Copyright (c) TaKo AI Sp. z o.o.

from typing import List

from src import DatabaseProvider
from src.domain.entities.business_entity import BusinessEntity
from src.domain.entities.client_entity import ClientEntity
from src.domain.entities.invoice_entity import InvoiceEntity
from src.domain.entities.product_entity import ProductEntity

from src.domain.repositories.invoice_repository_interface import (
    InvoiceRepositoryInterface,
)


class SQLInvoiceRepository(InvoiceRepositoryInterface):
    def __init__(self, database_provider: DatabaseProvider):
        self.database_provider = database_provider

    def get_all_invoices(self) -> List[InvoiceEntity]:
        invoices, businesses, clients, products_list = self.database_provider.invoice_list()

        invoice_entities = []
        for invoice, business, client, products in zip(invoices, businesses, clients, products_list):
            invoice_entity = InvoiceEntity(
                invoiceNo=invoice.invoiceNo,
                currency=invoice.currency,
                vatPercent=invoice.vatPercent,
                issuedAt=invoice.issuedAt,
                dueTo=invoice.dueTo,
                client=ClientEntity(**client.__dict__),
                business=BusinessEntity(**business.__dict__),
                note=invoice.note,
                products=[ProductEntity(**product.__dict__) for product in products],
                language=invoice.language
            )
            invoice_entities.append(invoice_entity)

        return invoice_entities

    def get_invoice_by_number(
        self, invoice_number: str, language: str
    ) -> InvoiceEntity | None:
        invoice = self.database_provider.invoice_get(invoice_number)
        if not invoice:
            return None

        return InvoiceEntity(**invoice.__dict__)

    def create_invoice(self, invoice: InvoiceEntity) -> None:

        self.database_provider.invoice_add(invoice)

    def update_invoice(self, invoice: InvoiceEntity) -> None:
        self.database_provider.invoice_put(invoice)

    def delete_invoice(self, invoice_number: str) -> None:
        self.database_provider.invoice_del(invoice_number)
