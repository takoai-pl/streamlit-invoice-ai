# Copyright (c) TaKo AI Sp. z o.o.

from importlib import metadata

from src.data.providers.database_provider import (
    DatabaseProvider,
)
from src.data.providers.database_schema import (
    BusinessTable,
    ClientTable,
    InvoiceTable,
    ProductTable,
)
from src.presentation.components.language_selector import build_language_selector
from src.presentation.components.file_uploader import build_file_uploader
from src.presentation.components.address_fields import build_address_fields

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
