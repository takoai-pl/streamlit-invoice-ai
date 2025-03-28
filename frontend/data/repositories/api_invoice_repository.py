# Copyright (c) TaKo AI Sp. z o.o.

from typing import List

from frontend.data.models import InvoiceModel
from frontend.data.providers import APIProvider
from frontend.domain.entities.invoice_entity import InvoiceEntity
from frontend.domain.repositories.invoice_repository_interface import (
    InvoiceRepositoryInterface,
)


class APIInvoiceRepository(InvoiceRepositoryInterface):
    def __init__(self, api_provider: APIProvider) -> None:
        self.api_provider = api_provider

    def get_all_invoices(self) -> List[InvoiceEntity]:
        invoices = self.api_provider.invoice_list()

        if not invoices:
            return []

        return [InvoiceEntity(**invoice.__dict__) for invoice in invoices]

    def get_invoice_by_number(
        self, invoice_number: str, language: str
    ) -> InvoiceEntity | None:
        invoice = self.api_provider.invoice_get(invoice_number, language)
        if not invoice:
            return None

        return InvoiceEntity(**invoice.__dict__)

    def create_invoice(self, invoice: InvoiceEntity) -> None:
        invoice = InvoiceModel(**invoice.__dict__)
        self.api_provider.invoice_add(invoice)

    def update_invoice(self, invoice: InvoiceEntity) -> None:
        invoice = InvoiceModel(**invoice.__dict__)
        self.api_provider.invoice_put(invoice)

    def delete_invoice(self, invoice_id: str) -> None:
        self.api_provider.invoice_del(invoice_id)
