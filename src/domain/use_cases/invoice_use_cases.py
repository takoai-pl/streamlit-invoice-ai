# Copyright (c) TaKo AI Sp. z o.o.

from src.domain import InvoiceEntity
from src.domain.repositories.invoice_repository_interface import (
    InvoiceRepositoryInterface,
)


class GetAllInvoicesUseCase:
    def __init__(self, invoice_repo: InvoiceRepositoryInterface):
        self.invoice_repo = invoice_repo

    def execute(self) -> list[InvoiceEntity]:
        return self.invoice_repo.get_all_invoices()


class AddInvoiceUseCase:
    def __init__(self, invoice_repo: InvoiceRepositoryInterface) -> None:
        self.invoice_repo = invoice_repo

    def execute(self, invoice: InvoiceEntity) -> None:
        self.invoice_repo.create_invoice(invoice)
