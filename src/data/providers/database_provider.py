# Copyright (c) TaKo AI Sp. z o.o.

from functools import wraps
from typing import Any, Callable, List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .database_schema import (
    BusinessTable,
    ClientTable,
    InvoiceTable,
)


def session_scope(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(self: "DatabaseProvider", *args: Any, **kwargs: Any) -> Any:
        session = self.Session()
        try:
            result = func(self, session, *args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.expunge_all()
            session.close()

    return wrapper


class DatabaseProvider:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)

    @session_scope
    def get_business(
        self, session: Session, business_name: str
    ) -> BusinessTable | None:
        return session.query(BusinessTable).filter_by(name=business_name).first()

    @session_scope
    def add_business(self, session: Session, business: BusinessTable) -> None:
        session.add(business)

    @session_scope
    def change_business_details(
        self, session: Session, business_name: str, business: BusinessTable
    ) -> None:
        business_table = (
            session.query(BusinessTable).filter_by(name=business_name).first()
        )
        if business_table is None:
            raise ValueError(f"No business found with name {business_name}")
        business_table.name = business.name
        business_table.street = business.street
        business_table.postCode = business.postCode
        business_table.town = business.town
        business_table.country = business.country
        business_table.vatNo = business.vatNo
        business_table.bic = business.bic
        business_table.iban = business.iban
        business_table.phone = business.phone
        business_table.email = business.email

    @session_scope
    def get_client(self, session: Session, client_name: str) -> ClientTable | None:
        return session.query(ClientTable).filter_by(name=client_name).first()

    @session_scope
    def add_client(self, session: Session, client: ClientTable) -> None:
        session.add(client)

    @session_scope
    def change_client_details(
        self, session: Session, client_name: str, client: ClientTable
    ) -> None:
        client_table = session.query(ClientTable).filter_by(name=client_name).first()
        if client_table is None:
            raise ValueError(f"No client found with name {client_name}")
        client_table.name = client.name
        client_table.street = client.street
        client_table.postCode = client.postCode
        client_table.town = client.town
        client_table.country = client.country
        client_table.vatNo = client.vatNo

    @session_scope
    def get_all_invoices(self, session: Session) -> List[InvoiceTable]:
        return session.query(InvoiceTable).all()
