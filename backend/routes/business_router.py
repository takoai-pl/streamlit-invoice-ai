import os
from typing import List

from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from backend.controllers import BusinessController
from backend.controllers.base_controller import (
    AlreadyExistsException,
    DatabaseConnectionException,
    NameCannotBeChangedException,
    NotFoundException,
    RetrievalException,
)
from backend.models import BusinessTable
from frontend.domain import BusinessEntity

business_router = APIRouter(
    tags=["business"],
    prefix="/business",
)

try:
    connection_string = os.getenv("POSTGRESQL_CONNECTION_STRING")
    if not connection_string:
        raise Exception("POSTGRESQL_CONNECTION_STRING environment variable not set")
    business_controller = BusinessController(connection_string)
except Exception as e:
    raise Exception(f"Failed to initialize business controller: {str(e)}")


@business_router.get("/", response_model=List[BusinessEntity])
async def get_list_of_businesses() -> JSONResponse:
    try:
        businesses = business_controller.list()
    except RetrievalException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseConnectionException as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    response = []
    for business in businesses:
        response.append(business.to_json())

    return JSONResponse(status_code=200, content=response)


@business_router.get("/{business_name}/", response_model=BusinessEntity)
async def get_business(business_name: str) -> JSONResponse:
    try:
        business = business_controller.get(business_name)
        if business is None:
            raise NotFoundException(business_name)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RetrievalException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseConnectionException as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    return JSONResponse(status_code=200, content=business.to_json())


@business_router.post("/")
async def add_business(data: dict) -> JSONResponse:
    try:
        business = BusinessTable.from_json(data)
        business_controller.add(business)
        return JSONResponse(status_code=201, content="Business created successfully")
    except AlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except RetrievalException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseConnectionException as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@business_router.put("/")
async def put_business(data: dict) -> JSONResponse:
    try:
        business = BusinessTable.from_json(data)
        business_controller.put(business)
        return JSONResponse(status_code=204, content="Business updated successfully")
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NameCannotBeChangedException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RetrievalException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseConnectionException as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@business_router.delete("/{business_name}/")
async def delete_business(business_name: str) -> JSONResponse:
    try:
        business_controller.delete(business_name)
        return JSONResponse(status_code=204, content="Business deleted successfully")
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RetrievalException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseConnectionException as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
