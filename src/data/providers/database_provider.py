# Copyright (c) TaKo AI Sp. z o.o.

from functools import wraps
from typing import Any, Callable, Type

from sqlalchemy import create_engine, and_
from sqlalchemy.exc import ArgumentError, OperationalError
from sqlalchemy.orm import Session, sessionmaker

from src.data.models.invoice_table import InvoiceTable
from src.data.models.client_table import ClientTable
from src.data.models import (
    BusinessTable,
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
            if isinstance(e, BusinessAlreadyExistsException):
                raise e
            if isinstance(e, BusinessNameCannotBeChangedException):
                raise e
            if isinstance(e, BusinessNotFoundException):
                raise e
            if isinstance(e, BusinessRetrievalException):
                raise e
            raise BusinessRetrievalException(f"Could not retrieve businesses: {str(e)}")
        finally:
            session.expunge_all()
            session.close()

    return wrapper


class DatabaseProvider:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        try:
            self.engine = create_engine(db_path)
            self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        except OperationalError as e:
            raise DatabaseConnectionException(
                f"Could not connect to the database: {str(e)}"
            )
        except ArgumentError as e:
            raise DatabaseConnectionException(
                f"Could not connect to the database: {str(e)}"
            )

    """ Business Section """

    @session_scope
    def business_list(
        self, session: Session
    ) -> list[Type[BusinessTable]] | list[BusinessTable]:
        return session.query(BusinessTable).all()

    @session_scope
    def business_get(
        self, session: Session, business_name: str
    ) -> BusinessTable | None:
        return session.query(BusinessTable).filter_by(name=business_name).first()

    @session_scope
    def business_add(self, session: Session, business: BusinessTable) -> None:
        existing_business = (
            session.query(BusinessTable).filter_by(name=business.name).first()
        )
        if existing_business:
            raise BusinessAlreadyExistsException(str(business.name))
        session.add(business)

    @session_scope
    def business_put(self, session: Session, business: BusinessTable) -> None:
        result = session.query(BusinessTable).filter_by(name=business.name).first()

        if result is None:
            raise BusinessNotFoundException(
                f"No business found with name {business.name}"
            )

        if result.name != business.name:
            raise BusinessNameCannotBeChangedException()

        for key, value in business.__dict__.items():
            if key != "_sa_instance_state":
                setattr(result, key, value)

    @session_scope
    def business_del(self, session: Session, business_name: str) -> None:
        business_table = (
            session.query(BusinessTable).filter_by(name=business_name).first()
        )
        if business_table is None:
            raise BusinessNotFoundException(
                f"No business found with name {business_name}"
            )
        session.delete(business_table)

    """ Client Section """

    @session_scope
    def client_list(
        self, session: Session
    ) -> list[Type[ClientTable]] | list[ClientTable]:
        return session.query(ClientTable).all()

    @session_scope
    def client_get(
        self, session: Session, client_name: str
    ) -> ClientTable | None:
        return session.query(ClientTable).filter_by(name=client_name).first()

    @session_scope
    def client_add(self, session: Session, client: ClientTable) -> None:
        existing_client = (
            session.query(ClientTable).filter_by(name=client.name).first()
        )
        if existing_client:
            raise ClientAlreadyExistsException(str(client.name))
        session.add(client)

    @session_scope
    def client_put(self, session: Session, client: ClientTable) -> None:
        result = session.query(ClientTable).filter_by(name=client.name).first()

        if result is None:
            raise ClientNotFoundException(
                f"No client found with name {client.name}"
            )

        if result.name != client.name:
            raise ClientNameCannotBeChangedException()

        for key, value in client.__dict__.items():
            if key != "_sa_instance_state":
                setattr(result, key, value)

    @session_scope
    def client_del(self, session: Session, client_name: str) -> None:
        client_table = (
            session.query(ClientTable).filter_by(name=client_name).first()
        )
        if client_table is None:
            raise ClientNotFoundException(
                f"No client found with name {client_name}"
            )
        session.delete(client_table)

    """ Invoice Methods """
    @session_scope
    def invoice_list(
        self, session: Session
    ) -> list[Type[InvoiceTable]] | list[InvoiceTable]:
        return session.query(InvoiceTable).all()

    @session_scope
    def invoice_get(
        self, session: Session, invoice_id: int
    ) -> InvoiceTable | None:
        return session.query(InvoiceTable).filter_by(id=invoice_id).first()

    @session_scope
    def invoice_add(self, session: Session, invoice: InvoiceTable) -> None:
        session.add(invoice)

    @session_scope
    def invoice_put(self, session: Session, invoice: InvoiceTable, language: str) -> None:
        result = session.query(InvoiceTable).filter(
            and_(
                InvoiceTable.invoiceId == invoice.invoiceNo,
                InvoiceTable.language == language
            )
        ).first()

        if result is None:
            raise InvoiceNotFoundException(
                f"No invoice found with id {invoice.invoiceNo}"
            )

        for key, value in invoice.__dict__.items():
            if key != "_sa_instance_state":
                setattr(result, key, value)

    @session_scope
    def invoice_del(self, session: Session, invoice_no: str) -> None:
        invoice_table = (
            session.query(InvoiceTable).filter_by(id=invoice_no).first()
        )
        if invoice_table is None:
            raise InvoiceNotFoundException(
                f"No invoice found with id {invoice_no}"
            )
        session.delete(invoice_table)


class DatabaseConnectionException(Exception):
    """Exception raised when there is an error connecting to the database."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class BusinessAlreadyExistsException(Exception):
    """Exception raised when a business with the given name already exists."""

    def __init__(self, business_name: str):
        self.business_name = business_name
        self.message = f"Business with name '{business_name}' already exists."
        super().__init__(self.message)


class BusinessNameCannotBeChangedException(Exception):
    """Exception raised when attempting to change the name of a business."""

    def __init__(self) -> None:
        self.message = "Business name cannot be changed."
        super().__init__(self.message)


class BusinessNotFoundException(Exception):
    """Exception raised when a business with the given name does not exist."""

    def __init__(self, business_name: str):
        self.business_name = business_name
        self.message = f"No business found with name {business_name}"
        super().__init__(self.message)


class BusinessRetrievalException(Exception):
    """Exception raised when there is an error retrieving businesses from the database."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ClientAlreadyExistsException(Exception):
    """Exception raised when a client with the given name already exists."""

    def __init__(self, client_name: str):
        self.client_name = client_name
        self.message = f"Client with name '{client_name}' already exists."
        super().__init__(self.message)


class ClientNameCannotBeChangedException(Exception):
    """Exception raised when attempting to change the name of a client."""

    def __init__(self) -> None:
        self.message = "Client name cannot be changed."
        super().__init__(self.message)


class ClientNotFoundException(Exception):
    """Exception raised when a client with the given name does not exist."""

    def __init__(self, client_name: str):
        self.client_name = client_name
        self.message = f"No client found with name {client_name}"
        super().__init__(self.message)


class ClientRetrievalException(Exception):
    """Exception raised when there is an error retrieving clients from the database."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class InvoiceNotFoundException(Exception):
    """Exception raised when an invoice with the given id does not exist."""

    def __init__(self, invoice_id: str):
        self.invoice_id = invoice_id
        self.message = f"No invoice found with id {invoice_id}"
        super().__init__(self.message)


class InvoiceRetrievalException(Exception):
    """Exception raised when there is an error retrieving invoices from the database."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)