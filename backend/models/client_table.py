# Copyright (c) TaKo AI Sp. z o.o.

import json
from typing import Any

from sqlalchemy import Column, String

from backend.models.base import Base


class ClientTable(Base):
    __tablename__ = "client"

    clientID = Column("clientID", String, primary_key=True, default=Base.generate_uuid)
    name = Column("name", String, unique=True)
    street = Column("street", String)
    postCode = Column("postCode", String)
    town = Column("town", String)
    country = Column("country", String)
    vatNo = Column("vatNo", String, unique=True)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = kwargs["name"]
        self.street = kwargs["street"]
        self.postCode = kwargs["postCode"]
        self.town = kwargs["town"]
        self.country = kwargs["country"]
        self.vatNo = kwargs["vatNo"]

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "street": self.street,
            "postCode": self.postCode,
            "town": self.town,
            "country": self.country,
            "vatNo": self.vatNo,
        }

    @staticmethod
    def from_json(data: dict) -> "ClientTable":
        client = ClientTable(
            name=data.get("name"),
            street=data.get("street"),
            postCode=data.get("postCode"),
            town=data.get("town"),
            country=data.get("country"),
            vatNo=data.get("vatNo"),
        )

        return client
