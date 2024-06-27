# Copyright (c) TaKo AI Sp. z o.o.

import os

from src.data.providers.database_provider import DatabaseProvider
from src.data.repositories.sql_business_repository import SQLBusinessRepository
from src.data.repositories.sql_clinet_repository import SQLClientRepository
from src.data.repositories.sql_invoice_repository import SQLInvoiceRepository
from src.domain import AddInvoiceUseCase, GetAllInvoicesUseCase
from src.domain.use_cases import (
    CreateBusinessUseCase,
    DeleteBusinessUseCase,
    EditBusinessUseCase,
    GetAllBusinessesNamesUseCase,
    GetAllClientsNamesUseCase,
    GetBusinessDetailsUseCase,
    GetClientDetailsUseCase,
    DownloadInvoiceUseCase,
)
from src.presentation.handler.handler import Handler
from src.utils import assets_path
from src.utils.generator import Generator

database_provider = DatabaseProvider(
    "sqlite:///" + os.path.join(assets_path, "demo_data")
)

generator = Generator()

business_repository = SQLBusinessRepository(database_provider)
client_repository = SQLClientRepository(database_provider)
invoice_repository = SQLInvoiceRepository(database_provider)

edit_business_use_case = EditBusinessUseCase(business_repository)
get_all_businesses_names_use_case = GetAllBusinessesNamesUseCase(business_repository)
get_business_details_use_case = GetBusinessDetailsUseCase(business_repository)
create_business_use_case = CreateBusinessUseCase(business_repository)
delete_business_use_case = DeleteBusinessUseCase(business_repository)

get_all_clients_names_use_case = GetAllClientsNamesUseCase(client_repository)
get_client_details_use_case = GetClientDetailsUseCase(client_repository)

get_all_invoices_use_case = GetAllInvoicesUseCase(invoice_repository)
add_invoice_use_case = AddInvoiceUseCase(invoice_repository)
download_invoice_use_case = DownloadInvoiceUseCase(generator)

handler = Handler(
    edit_business_use_case=edit_business_use_case,
    get_all_businesses_names_use_case=get_all_businesses_names_use_case,
    get_business_details_use_case=get_business_details_use_case,
    create_business_use_case=create_business_use_case,
    delete_business_use_case=delete_business_use_case,
    get_all_clients_names_use_case=get_all_clients_names_use_case,
    get_client_details_use_case=get_client_details_use_case,
    get_all_invoices_use_case=get_all_invoices_use_case,
    add_invoice_use_case=add_invoice_use_case,
    download_invoice_use_case=download_invoice_use_case
)
