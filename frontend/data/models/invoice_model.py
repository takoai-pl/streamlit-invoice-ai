# Copyright (c) TaKo AI Sp. z o.o.
from typing import Any

from frontend.domain import InvoiceEntity


class InvoiceModel(InvoiceEntity):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @classmethod
    def from_json(cls, json_data: dict) -> "InvoiceModel":
        return cls(**json_data)

    def to_json(
        self,
    ) -> dict:
        data = self.dict()
        if self.issuedAt:
            data["issuedAt"] = self.issuedAt.strftime("%d/%m/%Y")
        if self.dueTo:
            data["dueTo"] = self.dueTo.strftime("%d/%m/%Y")
        return data

    def to_entity(self) -> InvoiceEntity:
        return InvoiceEntity(**self.dict())
