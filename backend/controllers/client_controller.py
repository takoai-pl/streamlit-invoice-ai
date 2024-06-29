from typing import Type

from sqlalchemy.orm import Session

from backend.controllers.base_controller import (
    BaseController,
    ClientAlreadyExistsException,
    ClientNameCannotBeChangedException,
    ClientNotFoundException,
    session_scope,
)
from backend.models import ClientTable


class ClientController(BaseController):
    @session_scope
    def list(self, session: Session) -> list[Type[ClientTable]] | list[ClientTable]:
        return session.query(ClientTable).all()

    @session_scope
    def get(self, session: Session, client_name: str) -> ClientTable | None:
        return session.query(ClientTable).filter_by(name=client_name).first()

    @session_scope
    def add(self, session: Session, client: ClientTable) -> None:
        existing_client = session.query(ClientTable).filter_by(name=client.name).first()
        if existing_client:
            raise ClientAlreadyExistsException(str(client.name))
        session.add(client)

    @session_scope
    def put(self, session: Session, client: ClientTable) -> None:
        result = session.query(ClientTable).filter_by(name=client.name).first()

        if result is None:
            raise ClientNotFoundException(f"No client found with name {client.name}")

        if result.name != client.name:
            raise ClientNameCannotBeChangedException()

        for key, value in client.__dict__.items():
            if key != "_sa_instance_state":
                setattr(result, key, value)

    @session_scope
    def delete(self, session: Session, client_name: str) -> None:
        client_table = session.query(ClientTable).filter_by(name=client_name).first()
        if client_table is None:
            raise ClientNotFoundException(f"No client found with name {client_name}")
        session.delete(client_table)
