# Copyright (c) TaKo AI Sp. z o.o.

from typing import Optional

from pydantic import BaseModel


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
        if self.price is not None and self.vat is not None:
            return self.price * self.vat / 100
        else:
            return 0.0

    @property
    def sum(self) -> float:
        if self.price is not None and self.vat_amount is not None:
            return self.price + self.vat_amount
        else:
            return 0.0
