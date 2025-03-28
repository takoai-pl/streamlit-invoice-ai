# Copyright (c) TaKo AI Sp. z o.o.

import os

from frontend.data.providers import APIProvider
from frontend.data.repositories.api_business_repository import APIBusinessRepository
from frontend.data.repositories.api_client_repository import APIClientRepository
from frontend.data.repositories.api_invoice_repository import APIInvoiceRepository
from frontend.domain import (
    AddInvoiceUseCase,
    DeleteInvoiceUseCase,
    GetAllInvoicesUseCase,
    UpdateInvoiceUseCase,
)
from frontend.domain.use_cases import (
    CreateBusinessUseCase,
    CreateClientUseCase,
    DeleteBusinessUseCase,
    DeleteClientUseCase,
    DownloadInvoiceUseCase,
    GetAllBusinessesUseCase,
    GetAllClientsUseCase,
    GetBusinessDetailsUseCase,
    GetClientDetailsUseCase,
    UpdateBusinessUseCase,
    UpdateClientUseCase,
)
from frontend.presentation.handler.handler import Handler
from frontend.utils.generator import Generator

try:
    api_provider = APIProvider(os.getenv("BASE_URL"), os.getenv("API_KEY"))
except KeyError:
    raise Exception("environment variables not set")

generator = Generator()

business_repository = APIBusinessRepository(api_provider)
client_repository = APIClientRepository(api_provider)
invoice_repository = APIInvoiceRepository(api_provider)

update_business_use_case = UpdateBusinessUseCase(business_repository)
get_all_businesses_use_case = GetAllBusinessesUseCase(business_repository)
get_business_details_use_case = GetBusinessDetailsUseCase(business_repository)
create_business_use_case = CreateBusinessUseCase(business_repository)
delete_business_use_case = DeleteBusinessUseCase(business_repository)

get_all_clients_use_case = GetAllClientsUseCase(client_repository)
get_client_details_use_case = GetClientDetailsUseCase(client_repository)

get_all_invoices_use_case = GetAllInvoicesUseCase(invoice_repository)
add_invoice_use_case = AddInvoiceUseCase(invoice_repository)
download_invoice_use_case = DownloadInvoiceUseCase(generator)
update_invoice_use_case = UpdateInvoiceUseCase(invoice_repository)
delete_invoice_use_case = DeleteInvoiceUseCase(invoice_repository)

create_client_use_case = CreateClientUseCase(client_repository)
delete_client_use_case = DeleteClientUseCase(client_repository)
update_client_use_case = UpdateClientUseCase(client_repository)

handler = Handler(
    update_business_use_case=update_business_use_case,
    get_all_businesses_use_case=get_all_businesses_use_case,
    get_business_details_use_case=get_business_details_use_case,
    create_business_use_case=create_business_use_case,
    delete_business_use_case=delete_business_use_case,
    get_all_clients_use_case=get_all_clients_use_case,
    get_client_details_use_case=get_client_details_use_case,
    get_all_invoices_use_case=get_all_invoices_use_case,
    add_invoice_use_case=add_invoice_use_case,
    download_invoice_use_case=download_invoice_use_case,
    create_client_use_case=create_client_use_case,
    delete_client_use_case=delete_client_use_case,
    update_invoice_use_case=update_invoice_use_case,
    delete_invoice_use_case=delete_invoice_use_case,
    update_client_use_case=update_client_use_case,
)
