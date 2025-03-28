# Copyright (c) TaKo AI Sp. z o.o.

from abc import ABC, abstractmethod
from typing import List

from frontend.domain import InvoiceEntity


class InvoiceRepositoryInterface(ABC):
    @abstractmethod
    def get_all_invoices(self) -> List[InvoiceEntity]:
        pass

    @abstractmethod
    def get_invoice_by_number(
        self, invoice_number: str, language: str
    ) -> InvoiceEntity | None:
        pass

    @abstractmethod
    def create_invoice(self, invoice: InvoiceEntity) -> None:
        pass

    @abstractmethod
    def update_invoice(self, invoice: InvoiceEntity) -> None:
        pass

    @abstractmethod
    def delete_invoice(self, invoice_id: str) -> None:
        pass
