# Copyright (c) TaKo AI Sp. z o.o.

from typing import List


from frontend.domain.entities.business_entity import BusinessEntity
from frontend.domain.entities.client_entity import ClientEntity
from frontend.domain.entities.invoice_entity import InvoiceEntity
from frontend.domain.entities.product_entity import ProductEntity

from frontend.domain.repositories.invoice_repository_interface import (
    InvoiceRepositoryInterface,
)


class APIInvoiceRepository(InvoiceRepositoryInterface):
    def __init__(self, api_provider):
        self.database_provider = api_provider

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
