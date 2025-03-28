# Copyright (c) TaKo AI Sp. z o.o.

from typing import Optional

from pydantic import BaseModel

from frontend.utils.language import i18n as _


class ProductEntity(BaseModel):
    description: Optional[str] = ""
    quantity: Optional[int] = 0
    unit: Optional[str] = ""
    price: Optional[float] = 0.0
    vat: Optional[float] = 0.0

    @classmethod
    def validate_fields(cls, v: str, values: dict, field: str) -> None:
        if v is not None and any(value is None for value in values.values()):
            raise ValueError(f"If '{field}' is set, all other fields must also be set")

    @classmethod
    def validate_positive(cls, v: float, field: str) -> None:
        if v is not None and v < 0:
            raise ValueError(f"{field} must be positive")

    @property
    def vat_amount(self) -> float:
        if (
            self.price is not None
            and self.vat is not None
            and self.quantity is not None
        ):
            return self.price * self.quantity * self.vat / 100
        else:
            return 0.0

    @property
    def sum(self) -> float:
        if self.price is not None and self.quantity is not None:
            return self.price * self.quantity
        else:
            return 0.0

    def validate_product(self):
        if self.price is None:
            raise ValueError("Price must be set")
        if self.vat is None:
            raise ValueError("VAT must be set")
        if self.quantity is None:
            raise ValueError("Quantity must be set")
        if self.unit is None:
            raise ValueError("Unit must be set")
        if self.description is None:
            raise ValueError("Description must be set")
        if self.price < 0:
            raise ValueError("Price must be positive")
        if self.vat < 0:
            raise ValueError("VAT must be positive")
        if self.quantity < 0:
            raise ValueError("Quantity must be positive")
        if self.unit == "":
            raise ValueError("Unit must not be empty")
        if self.price == 0:
            raise ValueError("Price must not be zero")
        if self.quantity == 0:
            raise ValueError("Quantity must not be zero")
        return True
