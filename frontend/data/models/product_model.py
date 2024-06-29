# Copyright (c) TaKo AI Sp. z o.o.
from typing import Any

from pydantic import ValidationError

from frontend.domain import ProductEntity


class ProductModel(ProductEntity):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @classmethod
    def from_json(cls, json_data: dict) -> "ProductModel":
        try:
            return cls(**json_data)
        except ValidationError as e:
            raise ValueError(e)

    def to_json(
        self,
    ) -> dict:
        return self.dict()

    def to_entity(self) -> ProductEntity:
        return ProductEntity(**self.dict())
