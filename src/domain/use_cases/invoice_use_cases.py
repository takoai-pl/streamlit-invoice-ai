from src.domain import InvoiceEntity
from src.domain.repositories.invoice_repository_interface import InvoiceRepositoryInterface


class GetAllInvoicesUseCase:
    def __init__(self, invoice_repo: InvoiceRepositoryInterface):
        self.invoice_repo = invoice_repo

    def execute(self):
        return self.invoice_repo.get_all_invoices()


class AddInvoiceUseCase:
    def __init__(self, invoice_repo: InvoiceRepositoryInterface):
        self.invoice_repo = invoice_repo

    def execute(self, invoice: InvoiceEntity):
        self.invoice_repo.create_invoice(invoice)
