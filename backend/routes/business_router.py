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
from backend.utils.logger import setup_logger
from frontend.domain import BusinessEntity

logger = setup_logger("business_router")

business_router = APIRouter(
    tags=["business"],
    prefix="/business",
)

try:
    connection_string = os.getenv("POSTGRESQL_CONNECTION_STRING")
    if not connection_string:
        logger.error("POSTGRESQL_CONNECTION_STRING environment variable not set")
        raise Exception("POSTGRESQL_CONNECTION_STRING environment variable not set")
    business_controller = BusinessController(connection_string)
except Exception as e:
    logger.error(f"Failed to initialize business controller: {str(e)}", exc_info=True)
    raise Exception(f"Failed to initialize business controller: {str(e)}")


@business_router.get("/", response_model=List[BusinessEntity])
async def get_list_of_businesses() -> JSONResponse:
    try:
        businesses = business_controller.list()
    except RetrievalException as e:
        logger.error(f"Error retrieving businesses: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseConnectionException as e:
        logger.error(f"Database connection error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(
            f"Unexpected error in get_list_of_businesses: {str(e)}", exc_info=True
        )
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    response = []
    for business in businesses:
        response.append(business.to_json())

    return JSONResponse(status_code=200, content=response)


@business_router.get("/{business_id}/", response_model=BusinessEntity)
async def get_business(business_id: str) -> JSONResponse:
    try:
        business = business_controller.get(business_id)
        if business is None:
            logger.error(f"Business not found: {business_id}")
            raise NotFoundException(business_id)
    except NotFoundException as e:
        logger.error(f"Business not found: {str(e)}", exc_info=True)
        raise HTTPException(status_code=404, detail=str(e))
    except RetrievalException as e:
        logger.error(f"Error retrieving business: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseConnectionException as e:
        logger.error(f"Database connection error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_business: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    return JSONResponse(status_code=200, content=business.to_json())


@business_router.post("/")
async def add_business(data: dict) -> JSONResponse:
    try:
        business = BusinessTable.from_json(data)
        business_controller.add(business)
        logger.info(f"Business created successfully: {business.name}")
        return JSONResponse(status_code=201, content="Business created successfully")
    except AlreadyExistsException as e:
        logger.error(f"Business already exists: {str(e)}", exc_info=True)
        raise HTTPException(status_code=409, detail=str(e))
    except RetrievalException as e:
        logger.error(f"Error adding business: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseConnectionException as e:
        logger.error(f"Database connection error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in add_business: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@business_router.put("/")
async def put_business(data: dict) -> JSONResponse:
    try:
        business = BusinessTable.from_json(data)
        business_controller.put(business)
        logger.info(f"Business updated successfully: {business.name}")
        return JSONResponse(status_code=204, content="Business updated successfully")
    except NotFoundException as e:
        logger.error(f"Business not found for update: {str(e)}", exc_info=True)
        raise HTTPException(status_code=404, detail=str(e))
    except NameCannotBeChangedException as e:
        logger.error(f"Attempt to change business name: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except RetrievalException as e:
        logger.error(f"Error updating business: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseConnectionException as e:
        logger.error(f"Database connection error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in put_business: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@business_router.delete("/{business_id}/")
async def delete_business(business_id: str) -> JSONResponse:
    try:
        business_controller.delete(business_id)
        logger.info(f"Business deleted successfully: {business_id}")
        return JSONResponse(status_code=204, content="Business deleted successfully")
    except NotFoundException as e:
        logger.error(f"Business not found for deletion: {str(e)}", exc_info=True)
        raise HTTPException(status_code=404, detail=str(e))
    except RetrievalException as e:
        logger.error(f"Error deleting business: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseConnectionException as e:
        logger.error(f"Database connection error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in delete_business: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
