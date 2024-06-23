# Copyright (c) TaKo AI Sp. z o.o.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.data.providers.database_schema import Base

from .mocks.schema_mocks import (
    business_table_mock,
    client_table_mock,
    invoice_table_mock,
    product_table_mock,
)


def populate_database() -> str:
    db_path = "sqlite:///tests/mocks/mock.db"
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, expire_on_commit=False)
    session = Session()

    session.add(business_table_mock)
    session.add(client_table_mock)
    session.commit()

    session.add(invoice_table_mock)
    session.add(product_table_mock)
    session.commit()

    session.close()

    return db_path


def erase_database() -> None:
    db_path = "sqlite:///tests/mocks/mock.db"
    engine = create_engine(db_path)
    Base.metadata.drop_all(engine)
