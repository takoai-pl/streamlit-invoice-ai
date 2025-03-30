# Copyright (c) TaKo AI Sp. z o.o.

import hashlib
from typing import Tuple

from sqlalchemy.orm import Session

from backend.models.user_table import UserTable


class UserHandler:
    def get_by_username(self, session: Session, username: str) -> Tuple[UserTable, str]:
        """Get user by username"""
        user = session.query(UserTable).filter(UserTable.username == username).first()
        if not user:
            return None, "User not found"
        return user, None

    def verify_password(self, user: UserTable, password: str) -> bool:
        """Verify user password"""
        return user.password == password

    def create_user(
        self,
        session: Session,
        username: str,
        password: str,
        business_ids: list[str] = None,
    ) -> Tuple[UserTable, str]:
        """Create new user"""
        try:
            user = UserTable(
                username=username,
                password=password,
                business_ids=business_ids or [],
            )
            session.add(user)
            session.commit()
            return user, None
        except Exception as e:
            session.rollback()
            return None, f"Failed to create user: {str(e)}"

    def get_user_businesses(self, session: Session, user_id: str) -> list[str]:
        """Get list of business IDs user has access to"""
        user, error = self.get_by_id(session, user_id)
        if error:
            return []
        return user.business_ids

    def get_by_id(self, session: Session, user_id: str) -> Tuple[UserTable, str]:
        """Get user by ID"""
        user = session.query(UserTable).filter(UserTable.userID == user_id).first()
        if not user:
            return None, "User not found"
        return user, None
