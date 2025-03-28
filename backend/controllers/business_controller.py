from typing import Type

from sqlalchemy.orm import Session

from backend.controllers.base_controller import (
    AlreadyExistsException,
    BaseController,
    NameCannotBeChangedException,
    NotFoundException,
    session_scope,
)
from backend.models import BusinessTable


class BusinessController(BaseController):
    def __init__(self, db_path: str | None) -> None:
        if db_path is None:
            raise Exception("db_path cannot be None")
        super().__init__(db_path)

    @session_scope
    def list(self, session: Session) -> list[Type[BusinessTable]] | list[BusinessTable]:
        return session.query(BusinessTable).all()

    @session_scope
    def get(self, session: Session, business_name: str) -> BusinessTable | None:
        return session.query(BusinessTable).filter_by(name=business_name).first()

    @session_scope
    def add(self, session: Session, business: BusinessTable) -> None:
        existing_business = (
            session.query(BusinessTable).filter_by(name=business.name).first()
        )
        if existing_business:
            raise AlreadyExistsException(str(business.name))
        session.add(business)

    @session_scope
    def put(self, session: Session, business: BusinessTable) -> None:
        result = session.query(BusinessTable).filter_by(name=business.name).first()

        if result is None:
            raise NotFoundException(f"No business found with name {business.name}")

        if result.name != business.name:
            raise NameCannotBeChangedException()

        for key, value in business.__dict__.items():
            if key not in ["name", "_sa_instance_state"]:
                setattr(result, key, value)

        if hasattr(business, "logo") and business.logo is not None:
            result.logo = business.logo

    @session_scope
    def delete(self, session: Session, business_name: str) -> None:
        business_table = (
            session.query(BusinessTable).filter_by(name=business_name).first()
        )
        if business_table is None:
            raise NotFoundException(f"No business found with name {business_name}")
        session.delete(business_table)
