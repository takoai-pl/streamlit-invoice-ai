# Copyright (c) TaKo AI Sp. z o.o.
import re
from typing import Any, Optional

from pydantic import BaseModel


class BusinessEntity(BaseModel):
    businessID: Optional[str] = ""
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
    logo: Optional[str] = None

    # @classmethod
    # def validate_vat_no(cls, v: str) -> str:
    #     pattern = re.compile(r"\d{10}")
    #     if not pattern.fullmatch(v):
    #         raise ValueError("Invalid VAT number. It should be 10 digits")
    #     return v

    # @classmethod
    # def validate_id(cls, v: str) -> str:
    #     if not v:
    #         raise ValueError("Business ID must be set")
    #     return v

    def validate_business(self) -> None:
        try:
            self.are_all_fields_filled()
            # self.validate_vat_no(self.vatNo)
            # self.validate_id(self.businessID)
        except ValueError as e:
            raise ValueError(f"Validation failed: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error during validation: {str(e)}")

    def are_all_fields_filled(self) -> None:
        empty_fields = []

        def is_field_filled(value: Any, prefix: str = "") -> bool:
            if isinstance(value, BaseModel):
                return all(
                    is_field_filled(getattr(value, field), f"{prefix}.{field}")
                    for field in value.__fields__
                )
            if value in (None, "", []):
                empty_fields.append(prefix)
                return False
            return True

        business_fields_filled = all(
            is_field_filled(getattr(self, field), field) for field in self.__fields__
        )

        if not business_fields_filled:
            raise ValueError(
                f"The following fields cannot be empty: {', '.join(empty_fields)}"
            )
