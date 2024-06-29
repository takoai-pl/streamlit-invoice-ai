import os
from typing import List

from fastapi import APIRouter
from fastapi.openapi.models import Response

from backend.controllers import ClientController
from backend.models import ClientTable
from frontend.domain import ClientEntity

client_router = APIRouter(
    tags=["client"],
    prefix="/client",
)

client_controller = ClientController(os.environ["POSTGRESQL_CONNECTION_STRING"])


@client_router.get("/", response_model=List[ClientEntity])
async def get_list_of_clients() -> list:
    clients = client_controller.list()

    response = []
    for client in clients:
        response.append(client.to_json())

    return response


@client_router.get("/{client_name}", response_model=ClientEntity)
async def get_client(client_name: str) -> dict:
    client = client_controller.get(client_name)
    return client.to_json()


@client_router.post("/")
async def add_client(data: dict) -> Response:
    client = ClientTable.from_json(data)
    client_controller.add(client)

    return Response(status_code=201, content="Client created")


@client_router.put("/")
async def put_client(data: dict) -> Response:
    client = ClientTable.from_json(data)
    client_controller.put(client)

    return Response(status_code=204, content="Client updated")


@client_router.delete("/{client_name}")
async def delete_client(client_name: str) -> Response:
    client_controller.delete(client_name)

    return Response(status_code=204, content="Client deleted")
