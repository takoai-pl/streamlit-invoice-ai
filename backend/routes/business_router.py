import os
from typing import List

from fastapi import APIRouter
from starlette.responses import JSONResponse

from backend.controllers import BusinessController
from backend.models import BusinessTable
from frontend.domain import BusinessEntity

business_router = APIRouter(
    tags=["business"],
    prefix="/business",
)

try:
    business_controller = BusinessController(os.getenv("POSTGRESQL_CONNECTION_STRING"))
except KeyError:
    raise Exception("POSTGRESQL_CONNECTION_STRING environment variable not set")


@business_router.get("/", response_model=List[BusinessEntity])
async def get_list_of_businesses() -> JSONResponse:
    try:
        businesses = business_controller.list()
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))

    response = []
    for business in businesses:
        response.append(business.to_json())

    return JSONResponse(status_code=200, content=response)


@business_router.get("/{business_name}/", response_model=BusinessEntity)
async def get_business(business_name: str) -> JSONResponse:
    try:
        business = business_controller.get(business_name)
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))

    return JSONResponse(status_code=200, content=business.to_json())


@business_router.post("/")
async def add_business(data: dict) -> JSONResponse:
    try:
        BusinessEntity(**data).validate_business()
    except Exception as e:
        return JSONResponse(status_code=400, content=str(e))

    business = BusinessTable.from_json(data)

    try:
        business_controller.add(business)
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))

    return JSONResponse(status_code=201, content="Business created successfully")


@business_router.put("/")
async def put_business(data: dict) -> JSONResponse:
    try:
        BusinessEntity(**data).validate_business()
    except Exception as e:
        return JSONResponse(status_code=400, content=str(e))

    business = BusinessTable.from_json(data)

    try:
        business_controller.put(business)
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))

    return JSONResponse(status_code=204, content="Business updated successfully")


@business_router.delete("/{business_name}/")
async def delete_business(business_name: str) -> JSONResponse:
    try:
        business_controller.delete(business_name)
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))

    return JSONResponse(status_code=204, content="Business deleted successfully")
