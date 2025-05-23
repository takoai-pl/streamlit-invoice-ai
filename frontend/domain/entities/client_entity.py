# Copyright (c) TaKo AI Sp. z o.o.
from typing import Optional

from pydantic import BaseModel


class ClientEntity(BaseModel):
    clientID: Optional[str] = ""
    name: Optional[str] = ""
    street: Optional[str] = ""
    postCode: Optional[str] = ""
    town: Optional[str] = ""
    country: Optional[str] = ""
    vatNo: Optional[str] = ""

    @classmethod
    def validate_id(cls, v: str) -> str:
        if not v:
            raise ValueError("Client ID must be set")
        return v

    def validate_client(self) -> None:
        if self.clientID is None or self.clientID == "":
            raise ValueError("Client ID must be set")
        if self.name is None:
            raise ValueError("Name must be set")
        if self.street is None:
            raise ValueError("Street must be set")
        if self.postCode is None:
            raise ValueError("Post code must be set")
        if self.town is None:
            raise ValueError("Town must be set")
        if self.country is None:
            raise ValueError("Country must be set")
        if self.vatNo is None:
            raise ValueError("VAT number must be set")
        if self.name == "":
            raise ValueError("Name must not be empty")
        if self.street == "":
            raise ValueError("Street must not be empty")
        if self.postCode == "":
            raise ValueError("Post code must not be empty")
        if self.town == "":
            raise ValueError("Town must not be empty")
        if self.country == "":
            raise ValueError("Country must not be empty")
        if self.vatNo == "":
            raise ValueError("VAT number must not be empty")
