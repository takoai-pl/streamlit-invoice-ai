# Copyright (c) TaKo AI Sp. z o.o.

from typing import Optional

from pydantic import BaseModel


class Business(BaseModel):
    name: Optional[str] = ""
    street: Optional[str] = ""
    postCode: Optional[str] = ""
    town: Optional[str] = ""
    country: Optional[str] = ""
    bic: Optional[str] = ""
    vatNo: Optional[str] = ""
    iban: Optional[str] = ""
    phone: Optional[str] = ""
    email: Optional[str] = ""
