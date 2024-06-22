# Copyright (c) TaKo AI Sp. z o.o.

import re
from pydantic import BaseModel, field_validator, EmailStr
from typing import List, Optional
from datetime import datetime, date
from models.client import Client
from models.business import Business
from models.product import Product


class Invoice(BaseModel):
    invoiceNo: Optional[str] = ""
    currency: Optional[str] = ""
    vatPercent: Optional[int] = 0
    issuedAt: Optional[date] = None
    dueTo: Optional[date] = None
    client: Client = Client()
    business: Business = Business()
    note: Optional[str] = ""
    products: List[Product] = []

    @classmethod
    @field_validator('invoiceNo')
    def validate_invoice_no(cls, v):
        pattern = re.compile(r'\d{4}/\d{4}')
        if not pattern.fullmatch(v):
            raise ValueError('Invalid invoice number. It should be in the format XXXX/XXXX')
        return v

    @classmethod
    @field_validator('currency')
    def validate_currency(cls, v):
        if len(v) != 3 or not v.isupper():
            raise ValueError('Invalid currency. It should be 3 characters long and in uppercase')
        return v

    @classmethod
    @field_validator('issuedAt', 'dueTo')
    def validate_dates(cls, v):
        if not isinstance(v, (datetime, date)):
            raise ValueError('Invalid date. It should be a datetime or date object')
        return v

    @classmethod
    @field_validator('dueTo')
    def validate_due_date(cls, v, values):
        if 'issuedAt' in values and v is not None:
            if v < values['issuedAt']:
                raise ValueError('dueTo date must be after issuedAt date')
        return v

    @property
    def total(self):
        return sum(product.sum for product in self.products)

    @property
    def subtotal(self):
        return sum(product.price for product in self.products)

    @property
    def vat_value(self):
        return sum(product.vat_amount for product in self.products)

    @classmethod
    def from_json(cls, file_path: str):
        return cls.parse_file(file_path)

    def to_json(self, file_path: str):
        with open(file_path, 'w') as f:
            f.write(self.json())

    def edit_field(self, field: str, value):
        valid_fields = {'invoiceNo', 'currency', 'vatPercent', 'issuedAt', 'dueTo', 'note'}

        if field in valid_fields:
            setattr(self, field, value)
        else:
            raise ValueError(f"Invalid field: {field}")

    def edit_client(self, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                setattr(self.client, key, value)

    def edit_business(self, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                setattr(self.business, key, value)

    def edit_product(self, product_index: int, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                setattr(self.products[product_index], key, value)

    def add_product(self, description, quantity, unit, price):
        self.products.append(
            Product(description=description,
                    quantity=quantity,
                    unit=unit,
                    price=price)
        )

    def delete_product(self, product_index: int):
        if product_index < 0 or product_index >= len(self.products):
            raise ValueError(f"Invalid product index: {product_index}")
        del self.products[product_index]
