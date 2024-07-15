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
            if isinstance(e, AlreadyExistsException):
                raise e
            if isinstance(e, NameCannotBeChangedException):
                raise e
            if isinstance(e, NotFoundException):
                raise e
            if isinstance(e, RetrievalException):
                raise e
            raise RetrievalException(f"Could not retrieve businesses: {str(e)}")
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


class AlreadyExistsException(Exception):
    """Exception raised when an entry with the given name already exists."""

    def __init__(self, name: str):
        self.name = name
        self.message = f"Entry with name '{name}' already exists."
        super().__init__(self.message)


class NameCannotBeChangedException(Exception):
    """Exception raised when attempting to change the name."""

    def __init__(self) -> None:
        self.message = "Name cannot be changed."
        super().__init__(self.message)


class NotFoundException(Exception):
    """Exception raised when entry with the given name does not exist."""

    def __init__(self, name: str):
        self.name = name
        self.message = f"Entry with name '{name}' does not exist."
        super().__init__(self.message)


class RetrievalException(Exception):
    """Exception raised when there is an error retrieving from the database."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
