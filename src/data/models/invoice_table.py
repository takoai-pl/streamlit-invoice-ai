# Copyright (c) TaKo AI Sp. z o.o.

import json
from typing import Any

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from src.data.models.product_table import ProductTable
from src.data.models.base import Base
from src.domain.entities.invoice_entity import InvoiceEntity


class InvoiceTable(Base):
    __tablename__ = "invoice"

    invoiceId = Column(
        "invoiceId", String, primary_key=True, default=Base.generate_uuid
    )
    invoiceNo = Column("invoiceNo", String)
    currency = Column("currency", String)
    vatPercent = Column("vatPercent", Integer)
    issuedAt = Column("issuedAt", String)
    dueTo = Column("dueTo", String)
    note = Column("note", String)
    business_id = Column(Integer, ForeignKey("business.businessID"))
    client_id = Column(Integer, ForeignKey("client.clientID"))

    business = relationship("BusinessTable")
    client = relationship("ClientTable")

    language = Column("language", String)

    @classmethod
    def from_model(cls, invoice: InvoiceEntity) -> ("InvoiceTable", list[ProductTable]):
        return cls(**vars(invoice)), [ProductTable.from_entity(product) for product in invoice.products]

    @classmethod
    def to_model(cls, invoice: "InvoiceTable", products: list[ProductTable]) -> InvoiceEntity:
        return InvoiceEntity(**vars(invoice), products=[ProductTable.to_entity(product) for product in products])

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.invoiceNo = kwargs["invoiceNo"]
        self.currency = kwargs["currency"]
        self.vatPercent = kwargs["vatPercent"]
        self.issuedAt = kwargs["issuedAt"]
        self.dueTo = kwargs["dueTo"]
        self.note = kwargs["note"]
        self.business_id = kwargs["business_id"]
        self.client_id = kwargs["client_id"]
        self.language = kwargs["language"]

    def __repr__(self) -> str:
        return json.dumps(
            {
                "invoiceNo": self.invoiceNo,
                "currency": self.currency,
                "vatPercent": self.vatPercent,
                "issuedAt": self.issuedAt,
                "dueTo": self.dueTo,
                "note": self.note,
                "business_id": self.business_id,
                "client_id": self.client_id,
                "language": self.language,
            }
        )
