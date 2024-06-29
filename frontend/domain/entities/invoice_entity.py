# Copyright (c) TaKo AI Sp. z o.o.

import re
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from frontend.domain.entities.business_entity import BusinessEntity
from frontend.domain.entities.client_entity import ClientEntity
from frontend.domain.entities.product_entity import ProductEntity


class InvoiceEntity(BaseModel):
    invoiceNo: Optional[str] = ""
    currency: Optional[str] = ""
    vatPercent: Optional[int] = 0
    issuedAt: Optional[date] = None
    dueTo: Optional[date] = None
    client: ClientEntity = ClientEntity()
    business: BusinessEntity = BusinessEntity()
    note: Optional[str] = ""
    products: List[ProductEntity] = []
    language: Optional[str] = ""

    @classmethod
    def validate_invoice_no(cls, v: str) -> str:
        pattern = re.compile(r"\d{4}/\d{4}")
        if not pattern.fullmatch(v):
            raise ValueError(
                "Invalid invoice number. It should be in the format XXXX/XXXX"
            )
        return v

    @classmethod
    def validate_currency(cls, v: str) -> str:
        if len(v) != 3 or not v.isupper():
            raise ValueError(
                "Invalid currency. It should be 3 characters long and in uppercase"
            )
        return v

    @classmethod
    def validate_dates(cls, v: date) -> date:
        if not isinstance(v, (datetime, date)):
            raise ValueError("Invalid date. It should be a datetime or date object")
        return v

    @classmethod
    def validate_due_date(cls, v: date, values: Dict[str, Any]) -> date:
        if "issuedAt" in values and v is not None:
            if v < values["issuedAt"]:
                raise ValueError("dueTo date must be after issuedAt date")
        return v

    @property
    def total(self) -> float:
        return sum(product.sum for product in self.products if product.sum is not None)

    @property
    def subtotal(self) -> float:
        return sum(
            product.price for product in self.products if product.price is not None
        )

    @property
    def vat_value(self) -> float:
        return sum(
            product.vat_amount
            for product in self.products
            if product.vat_amount is not None
        )

    @classmethod
    def from_json(cls, file_path: str) -> "InvoiceEntity":
        return cls.parse_file(file_path)

    def to_json(self, file_path: str) -> None:
        with open(file_path, "w") as f:
            f.write(self.json())

    def set_language(self, language: str) -> None:
        self.language = language

    def edit_field(self, field: str, value: Any) -> None:
        valid_fields = {
            "invoiceNo",
            "currency",
            "vatPercent",
            "issuedAt",
            "dueTo",
            "note",
        }

        if field in valid_fields:
            setattr(self, field, value)
        else:
            raise ValueError(f"Invalid field: {field}")

    def edit_client(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if value is not None:
                setattr(self.client, key, value)

    def edit_business(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if value is not None:
                setattr(self.business, key, value)

    def edit_product(self, product_index: int, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if value is not None:
                setattr(self.products[product_index], key, value)

    def add_product(
        self, description: str, quantity: int, unit: str, price: float
    ) -> None:
        self.products.append(
            ProductEntity(
                description=description, quantity=quantity, unit=unit, price=price
            )
        )

    def delete_product(self, product_index: int) -> None:
        if product_index < 0 or product_index >= len(self.products):
            raise ValueError(f"Invalid product index: {product_index}")
        del self.products[product_index]

    def are_all_fields_filled(self) -> bool:
        empty_fields = []

        def is_field_filled(value: Any, prefix: str = "") -> bool:
            if isinstance(value, BaseModel):
                return all(
                    is_field_filled(getattr(value, field), f"{prefix}.{field}")
                    for field in value.__fields__
                )
            if isinstance(value, list):
                return all(is_field_filled(item, prefix) for item in value)
            if value in (None, "", []):
                empty_fields.append(prefix)
                return False
            return True

        invoice_fields_filled = all(
            is_field_filled(getattr(self, field), field) for field in self.__fields__
        )

        if not invoice_fields_filled:
            raise ValueError(
                f"The following fields cannot be empty: {', '.join(empty_fields)}"
            )

        return invoice_fields_filled
