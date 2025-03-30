import os
import pathlib

from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy import create_engine, inspect, text

from backend.routes.business_router import business_router
from backend.routes.client_router import client_router
from backend.routes.invoice_router import invoice_router
from backend.routes.user_router import user_router

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI(
    title="Invoice AI API",
    description="API for Invoice AI",
    version="0.2.0",
)


def get_api_key(request_api_key_header: str = Security(api_key_header)):
    if (
        request_api_key_header == API_KEY
        or request_api_key_header == f"Bearer {API_KEY}"
    ):
        return request_api_key_header
    else:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )


def check_and_create_tables():
    connection_string = os.getenv("POSTGRESQL_CONNECTION_STRING")
    if not connection_string:
        raise Exception("POSTGRESQL_CONNECTION_STRING environment variable not set")

    engine = create_engine(connection_string)
    inspector = inspect(engine)

    required_tables = ["business", "client", "invoice", "product"]

    existing_tables = inspector.get_table_names()
    missing_tables = [
        table for table in required_tables if table not in existing_tables
    ]

    if missing_tables:
        script_path = (
            pathlib.Path(__file__).parent.parent / "assets" / "database_propagata.sql"
        )
        with open(script_path, "r") as f:
            sql_script = f.read()

        with engine.connect() as connection:
            connection.execute(text(sql_script))
            connection.commit()


@app.on_event("startup")
async def startup_event():
    check_and_create_tables()


@app.get("/")
def read_root():
    return {"status": "ok"}


app.include_router(business_router, dependencies=[Depends(get_api_key)])
app.include_router(client_router, dependencies=[Depends(get_api_key)])
app.include_router(invoice_router, dependencies=[Depends(get_api_key)])
app.include_router(user_router, dependencies=[Depends(get_api_key)])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
