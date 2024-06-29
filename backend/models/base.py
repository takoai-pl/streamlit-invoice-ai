# Copyright (c) TaKo AI Sp. z o.o.

import uuid

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True

    @staticmethod
    def generate_uuid() -> str:
        return str(uuid.uuid4())
