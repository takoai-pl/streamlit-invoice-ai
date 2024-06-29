from functools import wraps
from typing import Any, Callable

from sqlalchemy import create_engine
from sqlalchemy.exc import ArgumentError, OperationalError
from sqlalchemy.orm import sessionmaker


def session_scope(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(self: "BaseController", *args: Any, **kwargs: Any) -> Any:
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


class BaseController:
    def __init__(self, db_path: str | None) -> None:
        if not db_path:
            raise DatabaseConnectionException("Database path not provided.")
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
