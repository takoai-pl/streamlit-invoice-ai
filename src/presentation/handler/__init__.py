# Copyright (c) TaKo AI Sp. z o.o.

import os

from src.data.providers.database_provider import DatabaseProvider
from src.data.repositories.sql_business_repository import SQLBusinessRepository
from src.data.repositories.sql_clinet_repository import SQLClientRepository

from src.domain.use_cases import (
    CreateBusinessUseCase,
    DeleteBusinessUseCase,
    EditBusinessUseCase,
    GetAllBusinessesNamesUseCase,
    GetBusinessDetailsUseCase,
    GetAllClientsNamesUseCase,
)
from src.presentation.handler.handler import Handler
from src.utils import assets_path

database_provider = DatabaseProvider(
    "sqlite:///" + os.path.join(assets_path, "demo_data")
)

business_repository = SQLBusinessRepository(database_provider)
client_repository = SQLClientRepository(database_provider)

edit_business_use_case = EditBusinessUseCase(business_repository)
get_all_businesses_names_use_case = GetAllBusinessesNamesUseCase(business_repository)
get_business_details_use_case = GetBusinessDetailsUseCase(business_repository)
create_business_use_case = CreateBusinessUseCase(business_repository)
delete_business_use_case = DeleteBusinessUseCase(business_repository)

get_all_clients_names_use_case = GetAllClientsNamesUseCase(client_repository)

handler = Handler(
    edit_business_use_case=edit_business_use_case,
    get_all_businesses_names_use_case=get_all_businesses_names_use_case,
    get_business_details_use_case=get_business_details_use_case,
    create_business_use_case=create_business_use_case,
    delete_business_use_case=delete_business_use_case,
    get_all_clients_names_use_case=get_all_clients_names_use_case,
)
