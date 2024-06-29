import os
from typing import List
from urllib.parse import unquote

from fastapi import APIRouter
from starlette.responses import JSONResponse

from backend.controllers import InvoiceController
from backend.models import InvoiceTable
from backend.routes.business_router import business_controller
from backend.routes.client_router import client_controller
from frontend.domain import InvoiceEntity

invoice_router = APIRouter(
    tags=["invoice"],
    prefix="/invoice",
)

try:
    invoice_controller = InvoiceController(os.getenv("POSTGRESQL_CONNECTION_STRING"))
except KeyError:
    raise Exception("POSTGRESQL_CONNECTION_STRING environment variable not set")


@invoice_router.get("/", response_model=List[InvoiceEntity])
async def get_list_of_invoices() -> list:
    invoices, businesses, clients, products = invoice_controller.list()

    response = []
    for invoice, business, client, product in zip(
        invoices, businesses, clients, products
    ):
        response.append(invoice.to_json(business, client, product))

    return response


@invoice_router.get("/{invoice_no}/{language}", response_model=InvoiceEntity)
async def get_invoice(invoice_no: str, language: str) -> dict:
    decoded_invoice_no = unquote(invoice_no)
    invoice, business, client, products = invoice_controller.get(
        decoded_invoice_no, language
    )
    return invoice.to_json(business, client, products)


@invoice_router.post("/")
async def add_invoice(data: dict) -> JSONResponse:
    business_id = business_controller.get(data["business"]["name"]).businessID
    client_id = client_controller.get(data["client"]["name"]).clientID
    invoice, products = InvoiceTable.from_json(data, business_id, client_id)
    invoice_controller.add(invoice, products)
    return JSONResponse(status_code=201, content="Invoice created")


@invoice_router.put("/")
async def put_invoice(data: dict) -> JSONResponse:
    business_id = business_controller.get(data["business"]["name"]).businessID
    client_id = client_controller.get(data["client"]["name"]).clientID
    invoice, products = InvoiceTable.from_json(data, business_id, client_id)
    invoice_controller.put(invoice.invoiceNo, products)
    return JSONResponse(status_code=204, content="Invoice updated")


@invoice_router.delete("/{invoice_no}/{language}")
async def delete_invoice(invoice_no: str, language: str) -> JSONResponse:
    decoded_invoice_no = unquote(invoice_no)
    invoice_controller.delete(decoded_invoice_no, language)
    return JSONResponse(status_code=204, content="Invoice deleted")
