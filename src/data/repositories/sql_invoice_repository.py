# Copyright (c) TaKo AI Sp. z o.o.

from typing import List

from src import DatabaseProvider
from src.domain import InvoiceEntity
from src.domain.repositories.invoice_repository_interface import (
    InvoiceRepositoryInterface,
)


class SQLInvoiceRepository(InvoiceRepositoryInterface):
    def __init__(self, database_provider: DatabaseProvider):
        self.database_provider = database_provider

    def get_all_invoices(self) -> List[InvoiceEntity]:
        return [
            InvoiceEntity(**invoice.__dict__)
            for invoice in self.database_provider.invoice_list()
        ]

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
