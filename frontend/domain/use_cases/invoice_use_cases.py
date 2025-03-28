# Copyright (c) TaKo AI Sp. z o.o.

from frontend.domain import InvoiceEntity
from frontend.domain.repositories.invoice_repository_interface import (
    InvoiceRepositoryInterface,
)
from frontend.utils.generator import Generator


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


class UpdateInvoiceUseCase:
    def __init__(self, invoice_repo: InvoiceRepositoryInterface) -> None:
        self.invoice_repo = invoice_repo

    def execute(self, invoice: InvoiceEntity) -> None:
        self.invoice_repo.update_invoice(invoice)


class DeleteInvoiceUseCase:
    def __init__(self, invoice_repo: InvoiceRepositoryInterface) -> None:
        self.invoice_repo = invoice_repo

    def execute(self, invoice_id: str) -> None:
        self.invoice_repo.delete_invoice(invoice_id)


class DownloadInvoiceUseCase:
    def __init__(self, generator: Generator) -> None:
        self.generator = generator

    def execute(self, invoice: InvoiceEntity) -> str | None:
        return self.generator.generate(invoice)
