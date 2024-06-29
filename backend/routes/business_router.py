import os
from typing import List

from fastapi import APIRouter
from fastapi.openapi.models import Response

from backend.controllers import BusinessController
from backend.models import BusinessTable
from frontend.domain import BusinessEntity

business_router = APIRouter(
    tags=["business"],
    prefix="/business",
)

business_controller = BusinessController(os.environ["POSTGRESQL_CONNECTION_STRING"])


@business_router.get("/", response_model=List[BusinessEntity])
async def get_list_of_businesses() -> list:
    businesses = business_controller.list()

    response = []
    for business in businesses:
        response.append(business.to_json())

    return response


@business_router.get("/{business_name}", response_model=BusinessEntity)
async def get_business(business_name: str) -> dict:
    business = business_controller.get(business_name)
    return business.to_json()


@business_router.post("/")
async def add_business(data: dict) -> Response:
    business = BusinessTable.from_json(data)
    business_controller.add(business)

    return Response(status_code=201, content="Business created")


@business_router.put("/")
async def put_business(data: dict) -> Response:
    business = BusinessTable.from_json(data)
    business_controller.put(business)

    return Response(status_code=204, content="Business updated")


@business_router.delete("/{business_name}")
async def delete_business(business_name: str) -> Response:
    business_controller.delete(business_name)

    return Response(status_code=204, content="Business deleted")