# Copyright (c) TaKo AI Sp. z o.o.

import re
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from frontend.domain.entities.business_entity import BusinessEntity
from frontend.domain.entities.client_entity import ClientEntity
from frontend.domain.entities.product_entity import ProductEntity


class InvoiceEntity(BaseModel):
    invoiceID: Optional[str] = ""
    invoiceNo: Optional[str] = ""
    currency: Optional[str] = ""
    vatPercent: Optional[int] = 0
    issuedAt: Optional[date] = None
    dueTo: Optional[date] = None
    client: ClientEntity = ClientEntity()
    business: BusinessEntity = BusinessEntity()
    note: Optional[str] = ""
    products: List[ProductEntity] = []

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
    def validate_dates(cls, v: Any) -> date:
        if v is None:
            raise ValueError("Date cannot be None")

        if isinstance(v, date):
            return v

        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%d/%m/%Y").date()
            except ValueError as e:
                try:
                    print(e)
                    return datetime.strptime(v, "%Y-%m-%d").date()
                except ValueError as e:
                    raise ValueError(
                        f"Invalid date format: '{v}'. Expected DD/MM/YYYY or YYYY-MM-DD. "
                        f"Error: {str(e)}"
                    )

        raise ValueError(
            f"Invalid date type: {type(v)}. Expected date object or string in DD/MM/YYYY or YYYY-MM-DD format"
        )

    @classmethod
    def validate_due_date(cls, v: date, values: Dict[str, Any]) -> date:
        if "issuedAt" in values and v is not None:
            if v < values["issuedAt"]:
                raise ValueError(
                    f"Due date ({v}) must be after issue date ({values['issuedAt']})"
                )
        return v

    @property
    def total(self) -> float:
        return sum(product.sum for product in self.products if product.sum is not None)

    @property
    def subtotal(self) -> float:
        return sum(product.sum for product in self.products if product.sum is not None)

    @property
    def vat_value(self) -> float:
        if self.vatPercent is None:
            return 0.0
        return self.subtotal * self.vatPercent / 100

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
            if field in ["issuedAt", "dueTo"] and isinstance(value, str):
                value = self.validate_dates(value)
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
        self.products.pop(product_index)

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

    def validate_invoice(self) -> None:
        try:
            self.are_all_fields_filled()
            self.validate_invoice_no(self.invoiceNo)
            self.validate_currency(self.currency)
            self.validate_dates(self.issuedAt)
            self.validate_dates(self.dueTo)
            self.validate_due_date(self.dueTo, {"issuedAt": self.issuedAt})
            for product in self.products:
                product.validate_product()
            self.client.validate_client()
            self.business.validate_business()
        except ValueError as e:
            raise ValueError(f"Validation failed: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error during validation: {str(e)}")
