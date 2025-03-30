# Copyright (c) TaKo AI Sp. z o.o.

from typing import Any

from sqlalchemy import ARRAY, Column, String

from backend.models.base import Base


class UserTable(Base):
    __tablename__ = "user"

    userID = Column("userID", String, primary_key=True, default=Base.generate_uuid)
    username = Column("username", String, unique=True)
    password = Column("password", String)
    business_ids = Column("business_ids", ARRAY(String))

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.username = kwargs["username"]
        self.password = kwargs["password"]
        self.business_ids = kwargs.get("business_ids", [])

    def to_json(self) -> dict:
        return {
            "userID": self.userID,
            "username": self.username,
            "business_ids": self.business_ids,
        }

    @staticmethod
    def from_json(data: dict) -> "UserTable":
        user = UserTable(
            userID=data.get("userID", Base.generate_uuid()),
            username=data.get("username"),
            password=data.get("password"),
            business_ids=data.get("business_ids", []),
        )
        return user
