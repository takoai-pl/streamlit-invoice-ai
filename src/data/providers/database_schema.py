# Copyright (c) TaKo AI Sp. z o.o.

import json
import uuid
from typing import Any

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
)

from src.domain.models import (
    Business,
)


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


class BusinessTable(Base):
    __tablename__ = "business"
    businessID = Column("businessID", String, primary_key=True, default=generate_uuid)
    name = Column("name", String, unique=True)
    street = Column("street", String)
    postCode = Column("postCode", String)
    town = Column("town", String)
    country = Column("country", String)
    vatNo = Column("vatNo", String, unique=True)
    bic = Column("bic", String, unique=True)
    iban = Column("iban", String)
    phone = Column("phone", String)
    email = Column("email", String)

    @classmethod
    def from_model(cls, business: Business) -> "BusinessTable":
        assert isinstance(business, Business)
        return cls(**vars(business))

    def __init__(cls, **kwargs: Any) -> None:
        cls.name = kwargs["name"]
        cls.street = kwargs["street"]
        cls.postCode = kwargs["postCode"]
        cls.town = kwargs["town"]
        cls.country = kwargs["country"]
        cls.vatNo = kwargs["vatNo"]
        cls.bic = kwargs["bic"]
        cls.iban = kwargs["iban"]
        cls.phone = kwargs["phone"]
        cls.email = kwargs["email"]

    def __repr__(self) -> str:
        return json.dumps(
            {
                "name": self.name,
                "street": self.street,
                "postCode": self.postCode,
                "town": self.town,
                "country": self.country,
                "vatNo": self.vatNo,
                "bic": self.bic,
                "iban": self.iban,
                "phone": self.phone,
                "email": self.email,
            }
        )


class ClientTable(Base):
    __tablename__ = "client"

    clientID = Column("clientID", String, primary_key=True, default=generate_uuid)
    name = Column("name", String, unique=True)
    street = Column("street", String)
    postCode = Column("postCode", String)
    town = Column("town", String)
    country = Column("country", String)
    vatNo = Column("vatNo", String, unique=True)

    def __init__(cls, **kwargs: Any) -> None:
        cls.name = kwargs["name"]
        cls.street = kwargs["street"]
        cls.postCode = kwargs["postCode"]
        cls.town = kwargs["town"]
        cls.country = kwargs["country"]
        cls.vatNo = kwargs["vatNo"]

    def __repr__(self) -> str:
        return json.dumps(
            {
                "name": self.name,
                "street": self.street,
                "postCode": self.postCode,
                "town": self.town,
                "country": self.country,
                "vatNo": self.vatNo,
            }
        )


class InvoiceTable(Base):
    __tablename__ = "invoice"

    invoiceId = Column("invoiceId", String, primary_key=True, default=generate_uuid)
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

    def __init__(cls, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        cls.invoiceNo = kwargs["invoiceNo"]
        cls.currency = kwargs["currency"]
        cls.vatPercent = kwargs["vatPercent"]
        cls.issuedAt = kwargs["issuedAt"]
        cls.dueTo = kwargs["dueTo"]
        cls.note = kwargs["note"]
        cls.business_id = kwargs["business_id"]
        cls.client_id = kwargs["client_id"]

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
            }
        )


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
