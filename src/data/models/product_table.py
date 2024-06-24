# Copyright (c) TaKo AI Sp. z o.o.

import json
from typing import Any

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.data.models.base import Base


class ProductTable(Base):
    __tablename__ = "product"

    productID = Column(
        "productID", String, primary_key=True, default=Base.generate_uuid
    )
    description = Column("description", String)
    quantity = Column("quantity", Float)
    unit = Column("unit", String)
    price = Column("price", Float)
    vatPercent = Column("vatPercent", Float)
    invoice_id = Column(Integer, ForeignKey("invoice.invoiceId"))

    invoice = relationship("InvoiceTable")

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.description = kwargs["description"]
        self.quantity = kwargs["quantity"]
        self.unit = kwargs["unit"]
        self.price = kwargs["price"]
        self.vatPercent = kwargs["vatPercent"]
        self.invoice_id = kwargs["invoice_id"]

    def __repr__(self) -> str:
        return json.dumps(
            {
                "description": self.description,
                "quantity": self.quantity,
                "unit": self.unit,
                "price": self.price,
                "vatPercent": self.vatPercent,
                "invoice_id": self.invoice_id,
            }
        )
