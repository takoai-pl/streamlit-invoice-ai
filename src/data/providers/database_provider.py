# Copyright (c) TaKo AI Sp. z o.o.

from functools import wraps
from typing import Any, Callable, Type

from sqlalchemy import create_engine
from sqlalchemy.exc import ArgumentError, OperationalError
from sqlalchemy.orm import Session, sessionmaker

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
