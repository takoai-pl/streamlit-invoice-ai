# Copyright (c) TaKo AI Sp. z o.o.

from .base import Base
from .business_table import BusinessTable
from .client_table import ClientTable
from .invoice_table import InvoiceTable
from .product_table import ProductTable

__all__ = ["BusinessTable", "ClientTable", "InvoiceTable", "ProductTable", "Base"]
