# Copyright (c) TaKo AI Sp. z o.o.

import json
from typing import Any

from sqlalchemy import Column, String

from src.data.models.base import Base


class ClientTable(Base):
    __tablename__ = "client"

    clientID = Column("clientID", String, primary_key=True, default=Base.generate_uuid)
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
