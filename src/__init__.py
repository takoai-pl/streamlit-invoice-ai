from importlib import metadata

from src.components.language_selector import build_language_selector
from src.components.file_uploader import build_file_uploader
from src.components.address_fields import build_address_fields
from src.infrastructure.providers.database_provider import (
    get_business,
    get_all_products,
    get_invoice_by_client,
    get_product_by_invoice
)
from src.infrastructure.providers.database_schema import (
    business_table,
    client_table,
    invoice_table,
    product_table
)

__all__ = [
    'build_language_selector',
    'build_file_uploader',
    'build_address_fields',
    'get_business',
    'get_all_products',
    'get_invoice_by_client',
    'get_product_by_invoice',
    'business_table',
    'client_table',
    'invoice_table',
    'product_table'
]

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    __version__ = ""
del metadata
