import os
import pathlib

from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy import create_engine, inspect, text

from backend.routes.business_router import business_router
from backend.routes.client_router import client_router
from backend.routes.invoice_router import invoice_router
from backend.routes.user_router import user_router
from backend.utils.logger import setup_logger

logger = setup_logger("server")

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
        logger.error("Invalid API key provided")
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )


def check_and_create_tables():
    try:
        connection_string = os.getenv("POSTGRESQL_CONNECTION_STRING")
        if not connection_string:
            logger.error("POSTGRESQL_CONNECTION_STRING environment variable not set")
            raise Exception("POSTGRESQL_CONNECTION_STRING environment variable not set")

        engine = create_engine(connection_string)
        inspector = inspect(engine)

        required_tables = ["business", "client", "invoice", "product"]

        existing_tables = inspector.get_table_names()
        missing_tables = [
            table for table in required_tables if table not in existing_tables
        ]

        if missing_tables:
            logger.info(f"Creating missing tables: {missing_tables}")
            script_path = (
                pathlib.Path(__file__).parent.parent
                / "assets"
                / "database_propagata.sql"
            )
            with open(script_path, "r") as f:
                sql_script = f.read()

            with engine.connect() as connection:
                connection.execute(text(sql_script))
                connection.commit()
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error during table creation: {str(e)}", exc_info=True)
        raise


@app.on_event("startup")
async def startup_event():
    try:
        check_and_create_tables()
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}", exc_info=True)
        raise


@app.get("/")
def read_root():
    return {"status": "ok"}


app.include_router(business_router, dependencies=[Depends(get_api_key)])
app.include_router(client_router, dependencies=[Depends(get_api_key)])
app.include_router(invoice_router, dependencies=[Depends(get_api_key)])
app.include_router(user_router, dependencies=[Depends(get_api_key)])

if __name__ == "__main__":
    try:
        import uvicorn

        logger.info("Starting server on host 0.0.0.0:8080")
        uvicorn.run(app, host="0.0.0.0", port=8080)
    except Exception as e:
        logger.error(f"Error starting the server: {str(e)}", exc_info=True)
        raise
