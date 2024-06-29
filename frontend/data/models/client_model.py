# Copyright (c) TaKo AI Sp. z o.o.
from typing import Any

from frontend.domain import ClientEntity


class ClientModel(ClientEntity):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @classmethod
    def from_json(cls, json_data: dict) -> "ClientModel":
        return cls(**json_data)

    def to_json(
        self,
    ) -> dict:
        return self.dict()

    def to_entity(self) -> ClientEntity:
        return ClientEntity(**self.dict())
