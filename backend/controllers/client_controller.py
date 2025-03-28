from typing import Type

from sqlalchemy.orm import Session

from backend.controllers.base_controller import (
    BaseController,
    NameCannotBeChangedException,
    NotFoundException,
    session_scope,
)
from backend.models import ClientTable


class ClientController(BaseController):
    @session_scope
    def list(self, session: Session) -> list[Type[ClientTable]] | list[ClientTable]:
        return session.query(ClientTable).all()

    @session_scope
    def get(self, session: Session, client_id: str) -> ClientTable | None:
        return session.query(ClientTable).filter_by(clientID=client_id).first()

    @session_scope
    def add(self, session: Session, client: ClientTable) -> None:
        existing_client = (
            session.query(ClientTable).filter_by(clientID=client.clientID).first()
        )
        if existing_client:
            raise str(client.clientID)
        session.add(client)

    @session_scope
    def put(self, session: Session, client: ClientTable) -> None:
        result = session.query(ClientTable).filter_by(clientID=client.clientID).first()

        if result is None:
            raise NotFoundException(f"No client found with ID {client.clientID}")

        for key, value in client.__dict__.items():
            if key not in ["clientID", "_sa_instance_state"]:
                setattr(result, key, value)

    @session_scope
    def delete(self, session: Session, client_id: str) -> None:
        client_table = session.query(ClientTable).filter_by(clientID=client_id).first()
        if client_table is None:
            raise NotFoundException(f"No client found with ID {client_id}")
        session.delete(client_table)
