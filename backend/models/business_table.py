# Copyright (c) TaKo AI Sp. z o.o.

import json
from typing import Any

from sqlalchemy import Column, String

from backend.models.base import Base


class BusinessTable(Base):
    __tablename__ = "business"
    businessID = Column(
        "businessID", String, primary_key=True, default=Base.generate_uuid
    )
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

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = kwargs["name"]
        self.street = kwargs["street"]
        self.postCode = kwargs["postCode"]
        self.town = kwargs["town"]
        self.country = kwargs["country"]
        self.vatNo = kwargs["vatNo"]
        self.bic = kwargs["bic"]
        self.iban = kwargs["iban"]
        self.phone = kwargs["phone"]
        self.email = kwargs["email"]

    def to_json(self) -> dict:
        return {
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

    @staticmethod
    def from_json(data: dict) -> "BusinessTable":
        business = BusinessTable(
            name=data.get("name"),
            street=data.get("street"),
            postCode=data.get("postCode"),
            town=data.get("town"),
            country=data.get("country"),
            vatNo=data.get("vatNo"),
            bic=data.get("bic"),
            iban=data.get("iban"),
            phone=data.get("phone"),
            email=data.get("email"),
        )

        return business

