from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import os

from backend.routes.business_router import business_router
from backend.routes.client_router import client_router
from backend.routes.invoice_router import invoice_router

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI(
    title="Invoice AI API",
    description="API for Invoice AI",
    version="0.2.0",
)


def get_api_key(request_api_key_header: str = Security(api_key_header)):
    print(request_api_key_header)
    print(Security(api_key_header))
    print(API_KEY)
    if request_api_key_header == API_KEY or request_api_key_header == f"Bearer {API_KEY}":
        return request_api_key_header
    else:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )


@app.get("/")
def read_root():
    return {"status": "ok"}


app.include_router(business_router, dependencies=[Depends(get_api_key)])
app.include_router(client_router, dependencies=[Depends(get_api_key)])
app.include_router(invoice_router, dependencies=[Depends(get_api_key)])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
