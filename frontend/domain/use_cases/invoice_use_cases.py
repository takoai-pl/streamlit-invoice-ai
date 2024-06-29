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


class DownloadInvoiceUseCase:
    def __init__(self, generator: Generator) -> None:
        self.generator = generator

    def execute(self, invoice: InvoiceEntity) -> bytes | None:
        return self.generator.download(invoice)
