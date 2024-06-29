# Copyright (c) TaKo AI Sp. z o.o.
from typing import Any

from frontend.domain import BusinessEntity


class BusinessModel(BusinessEntity):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @classmethod
    def from_json(cls, json_data: dict) -> "BusinessModel":
        return cls(**json_data)

    def to_json(
        self,
    ) -> dict:
        return self.dict()

    def to_entity(self) -> BusinessEntity:
        return BusinessEntity(**self.dict())
