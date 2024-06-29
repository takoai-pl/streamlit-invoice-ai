# Copyright (c) TaKo AI Sp. z o.o.
from frontend.domain import InvoiceEntity


class InvoiceModel(InvoiceEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_json(cls, json_data: dict) -> "InvoiceModel":
        return cls(**json_data)

    def to_json(self, ) -> dict:
        return self.dict()

    def to_entity(self) -> InvoiceEntity:
        return InvoiceEntity(**self.dict())
