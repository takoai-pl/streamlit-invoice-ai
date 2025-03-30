# Copyright (c) TaKo AI Sp. z o.o.

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

connection_string = os.getenv("POSTGRESQL_CONNECTION_STRING")
if not connection_string:
    raise Exception("POSTGRESQL_CONNECTION_STRING environment variable not set")

engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
