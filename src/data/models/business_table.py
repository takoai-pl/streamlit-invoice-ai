# Copyright (c) TaKo AI Sp. z o.o.

import json
from typing import Any

from sqlalchemy import Column, String

from src.data.models.base import Base
from src.domain.entities.business_entity import BusinessEntity


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

    @classmethod
    def from_model(cls, business: BusinessEntity) -> "BusinessTable":
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
