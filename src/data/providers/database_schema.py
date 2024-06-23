# Copyright (c) TaKo AI Sp. z o.o.

import json
import uuid

from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeMeta
from sqlalchemy.ext.declarative import declarative_base
from typing import TYPE_CHECKING, Any, Type

from src.domain.models import (
    Business,
    Client,
    Invoice,
    Product,
)


def get_base() -> Type[DeclarativeMeta]:
    return declarative_base()


Base: Type[DeclarativeMeta] = get_base()


def generate_uuid() -> str:
    return str(uuid.uuid4())


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
        cls.name = kwargs.get("name")
        cls.street = kwargs.get("street")
        cls.postCode = kwargs.get("postCode")
        cls.town = kwargs.get("town")
        cls.country = kwargs.get("country")
        cls.vatNo = kwargs.get("vatNo")
        cls.bic = kwargs.get("bic")
        cls.iban = kwargs.get("iban")
        cls.phone = kwargs.get("phone")
        cls.email = kwargs.get("email")

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
        super().__init__(**kwargs)
        cls.name = kwargs.get("name")
        cls.street = kwargs.get("street")
        cls.postCode = kwargs.get("postCode")
        cls.town = kwargs.get("town")
        cls.country = kwargs.get("country")
        cls.vatNo = kwargs.get("vatNo")

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
        cls.invoiceNo = kwargs.get("invoiceNo")
        cls.currency = kwargs.get("currency")
        cls.vatPercent = kwargs.get("vatPercent")
        cls.issuedAt = kwargs.get("issuedAt")
        cls.dueTo = kwargs.get("dueTo")
        cls.note = kwargs.get("note")
        cls.business_id = kwargs.get("business_id")
        cls.client_id = kwargs.get("client_id")

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
        self.description = kwargs.get("description")
        self.quantity = kwargs.get("quantity")
        self.unit = kwargs.get("unit")
        self.price = kwargs.get("price")
        self.vatPercent = kwargs.get("vatPercent")
        self.invoice_id = kwargs.get("invoice_id")

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
