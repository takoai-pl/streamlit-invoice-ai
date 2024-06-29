from fastapi import FastAPI
from langserve import add_routes

from backend.routes.business_router import business_router
from backend.routes.graph import get_chain

app = FastAPI(
    title="Invoice AI API",
    description="API for Invoice AI",
    version="0.1.0",
)

app.include_router(business_router)

add_routes(app, get_chain())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
