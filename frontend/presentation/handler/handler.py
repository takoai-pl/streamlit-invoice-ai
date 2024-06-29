# Copyright (c) TaKo AI Sp. z o.o.

from frontend.domain import (
    AddInvoiceUseCase,
    BusinessEntity,
    ClientEntity,
    CreateBusinessUseCase,
    DeleteBusinessUseCase,
    DownloadInvoiceUseCase,
    EditBusinessUseCase,
    GetAllBusinessesNamesUseCase,
    GetAllClientsNamesUseCase,
    GetAllInvoicesUseCase,
    GetBusinessDetailsUseCase,
    GetClientDetailsUseCase,
    InvoiceEntity,
)


class Handler:
    """Facade class for handling business use cases"""

    def __init__(
        self,
        edit_business_use_case: EditBusinessUseCase,
        get_all_businesses_names_use_case: GetAllBusinessesNamesUseCase,
        get_business_details_use_case: GetBusinessDetailsUseCase,
        create_business_use_case: CreateBusinessUseCase,
        delete_business_use_case: DeleteBusinessUseCase,
        get_all_clients_names_use_case: GetAllClientsNamesUseCase,
        get_client_details_use_case: GetClientDetailsUseCase,
        get_all_invoices_use_case: GetAllInvoicesUseCase,
        add_invoice_use_case: AddInvoiceUseCase,
        download_invoice_use_case: DownloadInvoiceUseCase,
    ):
        self.edit_business_use_case = edit_business_use_case
        self.get_all_businesses_names_use_case = get_all_businesses_names_use_case
        self.get_business_details_use_case = get_business_details_use_case
        self.create_business_use_case = create_business_use_case
        self.delete_business_use_case = delete_business_use_case
        self.get_all_clients_names_use_case = get_all_clients_names_use_case
        self.get_client_details_use_case = get_client_details_use_case
        self.get_all_invoices_use_case = get_all_invoices_use_case
        self.add_invoice_use_case = add_invoice_use_case
        self.download_invoice_use_case = download_invoice_use_case

    def edit_business(self, business: BusinessEntity) -> None:
        self.edit_business_use_case.execute(business)

    def get_all_businesses_names(self) -> list[str | None]:
        return self.get_all_businesses_names_use_case.execute()

    def get_business_details(self, business_name: str) -> BusinessEntity | None:
        return self.get_business_details_use_case.execute(business_name)

    def create_business(self, business: BusinessEntity) -> None:
        self.create_business_use_case.execute(business)

    def delete_business(self, business_name: str) -> None:
        self.delete_business_use_case.execute(business_name)

    def get_all_clients_names(self) -> list[str | None]:
        return self.get_all_clients_names_use_case.execute()

    def get_client_details(self, client_name: str) -> ClientEntity | None:
        return self.get_client_details_use_case.execute(client_name)

    def get_all_invoices(self) -> list[InvoiceEntity]:
        return self.get_all_invoices_use_case.execute()

    def add_invoice(self, invoice: InvoiceEntity) -> None:
        self.add_invoice_use_case.execute(invoice)

    def download_invoice(self, invoice: InvoiceEntity) -> None:
        self.download_invoice_use_case.execute(invoice)
