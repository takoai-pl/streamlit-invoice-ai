# Copyright (c) TaKo AI Sp. z o.o.

from importlib import metadata

from src.data.models.business_table import BusinessTable
from src.data.models.client_table import ClientTable
from src.data.models.invoice_table import InvoiceTable
from src.data.models.product_table import ProductTable
from src.data.providers.database_provider import (
    DatabaseProvider,
)
from src.presentation.widgets.address_fields import build_address_fields
from src.presentation.widgets.file_uploader import build_file_uploader
from src.presentation.widgets.language_selector import build_language_selector

__all__ = [
    "build_language_selector",
    "build_file_uploader",
    "build_address_fields",
    "DatabaseProvider",
    "BusinessTable",
    "ClientTable",
    "InvoiceTable",
    "ProductTable",
]

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    __version__ = ""
del metadata
