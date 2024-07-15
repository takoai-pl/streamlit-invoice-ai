# Copyright (c) TaKo AI Sp. z o.o.
import re
from typing import Optional

from pydantic import BaseModel


class BusinessEntity(BaseModel):
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

    def validate_business(self) -> None:
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
        if self.bic is None:
            raise ValueError("BIC must be set")
        if self.vatNo is None:
            raise ValueError("VAT number must be set")
        if self.iban is None:
            raise ValueError("IBAN must be set")
        if self.phone is None:
            raise ValueError("Phone number must be set")
        if self.email is None:
            raise ValueError("Email must be set")
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
        if self.bic == "":
            raise ValueError("BIC must not be empty")
        if self.vatNo == "":
            raise ValueError("VAT number must not be empty")
        if self.iban == "":
            raise ValueError("IBAN must not be empty")
        if self.phone == "":
            raise ValueError("Phone number must not be empty")
        if self.email == "":
            raise ValueError("Email must not be empty")
        if not re.match(r'^[A-Z]{2}\d{10}$', self.vatNo):
            raise ValueError("Invalid VAT number format. It must be two letters followed by 10 digits.")
        if not re.match(r'^[A-Z]{4}[A-Z]{2}\d{2}(\d{5}){2}(\d{11})?$', self.iban):
            raise ValueError("Invalid IBAN format. It must be in the format CCXXYYYYYYYYYYYYYYYYYYYYYYYYY")
        if not re.match(r'^\+\d{2}\d{9,12}$', self.phone):
            raise ValueError("Invalid phone number format. It must be in the format +CCXXXXXXXXX")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            raise ValueError("Invalid email format. It must be in the format X@X.XX")
