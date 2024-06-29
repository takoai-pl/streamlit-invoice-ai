# Copyright (c) TaKo AI Sp. z o.o.

import json
from typing import Any

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.models.base import Base


class ProductTable(Base):
    __tablename__ = "product"

    productID = Column(
        "productID", String, primary_key=True, default=Base.generate_uuid
    )
    description = Column("description", String)
    quantity = Column("quantity", Float)
    unit = Column("unit", String)
    price = Column("price", Float)
    invoice_id = Column(String, ForeignKey("invoice.invoiceID"))

    invoice = relationship("InvoiceTable")

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.description = kwargs["description"]
        self.quantity = kwargs["quantity"]
        self.unit = kwargs["unit"]
        self.price = kwargs["price"]
        self.invoice_id = kwargs["invoice_id"]

    def to_json(self) -> dict:
        return {
            "description": self.description,
            "quantity": self.quantity,
            "unit": self.unit,
            "price": self.price,
        }

    @staticmethod
    def from_json(data: dict, invoice_id: str) -> "ProductTable":
        product = ProductTable(
            description=data.get("description"),
            quantity=data.get("quantity"),
            unit=data.get("unit"),
            price=data.get("price"),
            invoice_id=invoice_id,
        )

        return product
