# Copyright (c) TaKo AI Sp. z o.o.

import json
from typing import Any

from sqlalchemy import Column, String

from src.data.models.base import Base
from src.domain import ClientEntity


class ClientTable(Base):
    __tablename__ = "client"

    clientID = Column("clientID", String, primary_key=True, default=Base.generate_uuid)
    name = Column("name", String, unique=True)
    street = Column("street", String)
    postCode = Column("postCode", String)
    town = Column("town", String)
    country = Column("country", String)
    vatNo = Column("vatNo", String, unique=True)

    @classmethod
    def from_model(cls, client: "ClientEntity") -> "ClientTable":
        return cls(**vars(client))

    @classmethod
    def to_model(cls, client: "ClientTable") -> "ClientEntity":
        return ClientEntity(**vars(client))

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = kwargs["name"]
        self.street = kwargs["street"]
        self.postCode = kwargs["postCode"]
        self.town = kwargs["town"]
        self.country = kwargs["country"]
        self.vatNo = kwargs["vatNo"]

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
