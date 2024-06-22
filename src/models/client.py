# Copyright (c) TaKo AI Sp. z o.o.

from typing import Optional
from pydantic import BaseModel


class Client(BaseModel):
    name: Optional[str] = ""
    street: Optional[str] = ""
    postCode: Optional[str] = ""
    town: Optional[str] = ""
    country: Optional[str] = ""
    vatNo: Optional[str] = ""
