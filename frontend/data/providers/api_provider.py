# Copyright (c) TaKo AI Sp. z o.o.
from typing import List
from urllib.parse import quote

import requests

from frontend.data.models import BusinessModel, ClientModel, InvoiceModel


class APIProvider:
    def __init__(self, base_url: str | None):
        # TODO: Add error handling to the functions

        if not base_url:
            raise Exception("BASE_URL environment variable not set")
        self.base_url = base_url

    def invoice_list(self) -> List[InvoiceModel]:
        response = requests.get(f"{self.base_url}/invoice/")

        return [InvoiceModel.from_json(invoice) for invoice in response.json()]

    def invoice_get(self, invoice_no: str, language: str) -> InvoiceModel:
        encoded_invoice_no = quote(invoice_no, safe="")
        response = requests.get(
            f"{self.base_url}/invoice/{encoded_invoice_no}/{language}/"
        )
        return InvoiceModel.from_json(response.json())

    def invoice_add(self, invoice: InvoiceModel) -> None:
        requests.post(f"{self.base_url}/invoice/", json=invoice.to_json())

    def invoice_put(self, invoice: InvoiceModel) -> None:
        requests.put(f"{self.base_url}/invoice/", json=invoice.to_json())

    def invoice_del(self, invoice_no: str, language: str) -> None:
        encoded_invoice_no = quote(invoice_no, safe="")
        requests.delete(f"{self.base_url}/invoice/{encoded_invoice_no}/{language}/")

    def business_list(self) -> List[BusinessModel]:
        response = requests.get(f"{self.base_url}/business/")
        return [BusinessModel.from_json(business) for business in response.json()]

    def business_get(self, business_name: str) -> BusinessModel:
        response = requests.get(f"{self.base_url}/business/{business_name}/")
        return BusinessModel.from_json(response.json())

    def business_add(self, business: BusinessModel) -> None:
        requests.post(f"{self.base_url}/business/", json=business.to_json())

    def business_put(self, business: BusinessModel) -> None:
        requests.put(
            f"{self.base_url}/business/{business.name}/", json=business.to_json()
        )

    def business_del(self, business_name: str) -> None:
        requests.delete(f"{self.base_url}/business/{business_name}/")

    def client_list(self) -> List[ClientModel]:
        response = requests.get(f"{self.base_url}/client/")
        return [ClientModel.from_json(client) for client in response.json()]

    def client_get(self, client_name: str) -> ClientModel:
        response = requests.get(f"{self.base_url}/client/{client_name}/")
        return ClientModel.from_json(response.json())

    def client_add(self, client: ClientModel) -> None:
        requests.post(f"{self.base_url}/client/", json=client.to_json())

    def client_put(self, client: ClientModel) -> None:
        requests.put(f"{self.base_url}/client/{client.name}/", json=client.to_json())

    def client_del(self, client_name: str) -> None:
        requests.delete(f"{self.base_url}/client/{client_name}/")
