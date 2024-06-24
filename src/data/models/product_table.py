import json
import uuid

from typing import (
    Any
)

from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import (
    DeclarativeBase,
    relationship
)


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


class ProductTable(Base):
    __tablename__ = "product"

    productID = Column("productID", String, primary_key=True, default=generate_uuid)
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