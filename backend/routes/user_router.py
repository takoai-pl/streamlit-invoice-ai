# Copyright (c) TaKo AI Sp. z o.o.

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.handlers.user_handler import UserHandler

user_router = APIRouter(prefix="/user", tags=["user"])


class LoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    userID: str
    username: str
    business_ids: List[str]


@user_router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user_handler = UserHandler()
    user, error = user_handler.get_by_username(db, request.username)
    if error:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user_handler.verify_password(user, request.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return UserResponse(**user.to_json())


@user_router.get("/businesses/{user_id}")
def get_user_businesses(user_id: str, db: Session = Depends(get_db)):
    user_handler = UserHandler()
    business_ids = user_handler.get_user_businesses(db, user_id)
    return {"business_ids": business_ids}
