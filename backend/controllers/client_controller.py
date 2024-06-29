from typing import Type

from sqlalchemy.orm import Session


from backend.controllers.base_controller import BaseController, session_scope
from backend.models import ClientTable


class ClientController(BaseController):
    @session_scope
    def client_list(
            self, session: Session
    ) -> list[Type[ClientTable]] | list[ClientTable]:
        return session.query(ClientTable).all()

    @session_scope
    def client_get(self, session: Session, client_name: str) -> ClientTable | None:
        return session.query(ClientTable).filter_by(name=client_name).first()

    @session_scope
    def client_add(self, session: Session, client: ClientTable) -> None:
        existing_client = session.query(ClientTable).filter_by(name=client.name).first()
        if existing_client:
            raise ClientAlreadyExistsException(str(client.name))
        session.add(client)

    @session_scope
    def client_put(self, session: Session, client: ClientTable) -> None:
        result = session.query(ClientTable).filter_by(name=client.name).first()

        if result is None:
            raise ClientNotFoundException(f"No client found with name {client.name}")

        if result.name != client.name:
            raise ClientNameCannotBeChangedException()

        for key, value in client.__dict__.items():
            if key != "_sa_instance_state":
                setattr(result, key, value)

    @session_scope
    def client_del(self, session: Session, client_name: str) -> None:
        client_table = session.query(ClientTable).filter_by(name=client_name).first()
        if client_table is None:
            raise ClientNotFoundException(f"No client found with name {client_name}")
        session.delete(client_table)


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
