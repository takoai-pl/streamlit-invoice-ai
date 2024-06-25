# tests/mocks/populate_database_mock.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.data.models.base import Base
from tests.mocks.schema_mocks import (
    business_table_mock,
    client_table_mock,
    invoice_table_mock,
    product_table_mock,
)


def populate_database() -> str:
    db_file = os.path.join(os.path.dirname(__file__), "mock.db")
    db_path = f"sqlite:///{db_file}"
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
    db_file = os.path.join(os.path.dirname(__file__), "mock.db")
    db_path = f"sqlite:///{db_file}"
    engine = create_engine(db_path)
    Base.metadata.drop_all(engine)
