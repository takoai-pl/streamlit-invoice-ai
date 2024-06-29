import os
from typing import List

from fastapi import APIRouter

from backend.controllers.business_controller import BusinessController
from frontend.domain import BusinessEntity

from dotenv import load_dotenv

load_dotenv(".env")

os.environ["POSTGRESQL_CONNECTION_STRING"] = os.getenv("POSTGRESQL_CONNECTION_STRING")
print(os.getenv("POSTGRESQL_CONNECTION_STRING"))
business_router = APIRouter(
    tags=["business"],
    prefix="/business",
)

controller = BusinessController(os.getenv("POSTGRESQL_CONNECTION_STRING"))


@business_router.get("/get", response_model=List[BusinessEntity])
async def get_list(self):
    return self.controller.list()


