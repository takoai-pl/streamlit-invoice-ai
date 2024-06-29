from functools import wraps
from typing import Callable, Any

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, ArgumentError
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