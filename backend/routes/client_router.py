import os
from typing import List

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.controllers import ClientController
from backend.models import ClientTable
from frontend.domain import ClientEntity

client_router = APIRouter(
    tags=["client"],
    prefix="/client",
)

try:
    client_controller = ClientController(os.environ["POSTGRESQL_CONNECTION_STRING"])
except KeyError:
    raise Exception("POSTGRESQL_CONNECTION_STRING environment variable not set")


@client_router.get("/", response_model=List[ClientEntity])
async def get_list_of_clients() -> JSONResponse:
    clients = client_controller.list()

    response = []
    for client in clients:
        response.append(client.to_json())

    return JSONResponse(status_code=200, content=response)


@client_router.get("/{client_name}/", response_model=ClientEntity)
async def get_client(client_name: str) -> JSONResponse:
    client = client_controller.get(client_name)

    return JSONResponse(status_code=200, content=client.to_json())


@client_router.post("/")
async def add_client(data: dict) -> JSONResponse:
    client = ClientTable.from_json(data)
    client_controller.add(client)

    return JSONResponse(status_code=201, content="Client created")


@client_router.put("/")
async def put_client(data: dict) -> JSONResponse:
    client = ClientTable.from_json(data)
    client_controller.put(client)

    return JSONResponse(status_code=204, content="Client updated")


@client_router.delete("/{client_name}/")
async def delete_client(client_name: str) -> JSONResponse:
    client_controller.delete(client_name)

    return JSONResponse(status_code=204, content="Client deleted")
