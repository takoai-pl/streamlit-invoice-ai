# Copyright (c) TaKo AI Sp. z o.o.

from typing import Optional
from pydantic import BaseModel, field_validator, ValidationError


class Product(BaseModel):
    description: Optional[str] = ""
    quantity: Optional[int] = 0
    unit: Optional[str] = ""
    price: Optional[float] = 0.0
    vat: Optional[float] = 0.0

    @classmethod
    @field_validator('description', 'quantity', 'unit', 'price', 'vat')
    def validate_fields(cls, v, values, field):
        if v is not None and any(value is None for value in values.values()):
            raise ValidationError(f"If '{field}' is set, all other fields must also be set")
        return v

    @classmethod
    @field_validator('vat', 'price', 'quantity', 'unit')
    def validate_positive(cls, v, values, field):
        if v is not None and v < 0:
            raise ValueError(f"{field} must be positive")
        return v

    @property
    def vat_amount(self):
        return self.price * self.vat / 100

    @property
    def sum(self):
        return self.price + self.vat_amount
